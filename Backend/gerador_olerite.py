from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm
from io import BytesIO
from gerar_sub_total_um import Sub_total_um
from openpyxl import Workbook
from openpyxl import Workbook, load_workbook
import os
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from pymongo import MongoClient
from bson import ObjectId
from salvar_dados_mongo import MongoDBHandler  # Importe a classe MongoDBHandler
import logging


# Configuração básica de logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class Gerar_olerite:
    def __init__(self, funcao):
        self.funcao = funcao
        self.margin = 20  # Margens em mm
        self.page_width, self.page_height = A4  
        self.mongo_handler = MongoDBHandler('FUNCIONARIOS_VR3_PAGAMENTOS', 'pagamentos_periodo')
        logging.info("Classe Gerar_olerite inicializada com sucesso.")

   

    def converter_datas(dado):
        for key, value in dado.items():
            if isinstance(value, datetime.date):  # Verifica se o valor é do tipo datetime.date
                dado[key] = datetime.combine(value, datetime.min.time())  # Converte para datetime.datetime
        return dado


    def gerar_sub_um(self):
        logging.info("Iniciando geração do PDF.")
        try:
            # Calcular pagamento
            total_pagamento = Sub_total_um.calcular_pagamento_um(self.funcao)
            logging.debug(f"Total pagamento calculado: {total_pagamento}")

            # Validar se o pagamento é válido
            if total_pagamento['sub_total_tres'] is None:
                logging.warning("Pagamento nulo. Processo interrompido.")
                return None

            # Geração do PDF
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4,
                                    leftMargin=0,  # Margem esquerda
                                    rightMargin=0,  # Margem direita
                                    topMargin=30,  # Margem superior
                                    bottomMargin=30)  # Margem inferior

            elements = []
            self._draw_header(elements)
            content = self._prepare_content(total_pagamento)
            elements.append(self._create_table(content))
            self._draw_footer(elements)

            doc.build(elements)
            buffer.seek(0)
            logging.info("Dados enviados para o MongoDB com sucesso.")
            
        

            # Dados a serem salvos no MongoDB
            dados = {
                "nome": self.funcao.funcionario['nome_funcionario'],
                "equipe": self.funcao.funcionario['equipe'],
                "funcao": self.funcao.funcionario['nome_funcao'],
                "cpf": self.funcao.funcionario['numero_cpf'],
                "chave_pix": self.funcao.funcionario['chave_pix'],
                "valor_bruto": round(total_pagamento['sub_total_bruto'], 2),
                "valor_vale": round(total_pagamento['sub_total_dois_onze'], 2),
                "valor_total": round(total_pagamento['sub_total_tres'], 2) ,
                "data_inicio": self.funcao.data_inicio.strftime('%d/%m/%y'),
                "data_fim": self.funcao.data_fim.strftime('%d/%m/%y')
            }
           

            # Inserir no MongoDB
            id_salvo = self.mongo_handler.inserir_ou_atualizar_dado(dados)
            logging.info(f"Dados salvos no MongoDB com ID: {id_salvo}")

            return buffer
        
        except Exception as e:
            logging.error(f"Erro ao ao salvar os dados nos mongoDB: {str(e)}", exc_info=True)
            raise

    def _draw_header(self, elements):
        total_pagamento = self.funcao.calcular_pagamento_um()

        valor_sub_total_tres = total_pagamento.get('sub_total_tres')
      
        
        
        header = [
            ["JF COMERCIO E ENGENHARIA LTDA", "", ""],
            ["CNPJ: 45.528.735/0001-20", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["R E C I B O","", f"VALOR: R$ {valor_sub_total_tres:.2f}"],
            ["", "", ""],
            [f"RECEBI DE JF COMERCIO E ENGENHARIA LTDA A QUANTIA DE R$: {total_pagamento['sub_total_tres']:.2f}","",""],

            ["", "", ""]
            
            
        ]
        header_table = Table(header)
        header_table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                           ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                                           ('ALIGN', (5, 0), (5, 0), 'LEFT'), 
                                           ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                           ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                           ('FONTSIZE', (0, 0), (-1, -1), 11)]))
                                            
        
        elements.append(header_table)

    def _prepare_content(self, total_pagamento):
        data_inicio_formatada = (self.funcao.data_inicio).strftime('%d/%m/%Y') 
        data_fim_formatada = (self.funcao.data_fim).strftime('%d/%m/%Y')

        return [
            [f"PROVENTOS DE PRESTAÇÃO DE SERVIÇOS NO PERÍODO DE", f"{data_inicio_formatada}","Até", f"{data_fim_formatada}"],
            [f"NOME: {self.funcao.funcionario['nome_funcionario']}", "    QUAT.  VL R$","","PROVENTO"],
            [f"HORAS TRABALHADAS:", f"{self.funcao.horas_trabalhadas:.2f}  X  {self.funcao.funcionario['valor_hora_base']:.2f}","=", f"{total_pagamento['pagamento_base']:.2f}"],
            [f"REPOUSO REMUNERADO:", f"{self.funcao.repouso_remunerado:.2f}  X  {self.funcao.funcionario['repouso_remunerado']:.2f}","=", f"{total_pagamento['pagamento_folga_remunerada']:.2f}"],
            [f"HORAS EXTRAS DE 50%:", f"{self.funcao.horas_extras_um:.2f}  X  {self.funcao.funcionario['valor_hora_extra_um']:.2f}","=", f"{total_pagamento['pagamento_horas_extras_um']:.2f}"],
            [f"HORAS EXTRAS DE 100%:", f"{self.funcao.horas_extras_dois:.2f}  X  {self.funcao.funcionario['valor_hora_extra_dois']:.2f}","=", f"{total_pagamento['pagamento_horas_extras_dois']:.2f}"],
            [f"ADICIONAL NOTURNO:", f"{self.funcao.horas_noturnas:.2f}  X  {self.funcao.funcionario['adicional_noturno']:.2f}","=", f"{total_pagamento['pagamento_adicional_noturno']:.2f}"],
            [f"SUB-TOTAL 1:","","", f"{total_pagamento['sub_total_um']:.2f}",],
            [f"PAG. FÉRIAS ({self.funcao.funcionario['valor_ferias']:.2f}%):","","", f"{total_pagamento['sub_total_um_um']:.2f}", ],
            [f"PAG. 1/3 FÉRIAS ({self.funcao.funcionario['valor_um_terco_ferias']:.2f}%):", "","",f"{total_pagamento['sub_total_um_dois']:.2f}", ],
            [f"PAG. 13° SALÁRIO ({self.funcao.funcionario['valor_decimo_terceiro']:.2f}%):","","", f"{total_pagamento['sub_total_um_tres']:.2f}", ],
            [f"PAG FGTS ({self.funcao.funcionario['pagamento_fgts']:.2f}%):","","", f"{total_pagamento['sub_total_um_cinco']:.2f}", ],
            [f"SUB-TOTAL 2","","", f"{total_pagamento['sub_total_dois']:.2f}",],
            [f"PAG. INSS ({self.funcao.funcionario['desconto_inss']:.2f}%):","","", f"{total_pagamento['sub_total_dois_seis']:.2f}"],
            [f"DESC. REFEIÇÃO ({self.funcao.funcionario['desconto_refeicao']:.2f}% de Hs Trab + Repouso):","","", f"{total_pagamento['sub_total_dois_sete']:.2f}"],
            [f"DESC.TRANSPORTE ({self.funcao.funcionario['desconto_transporte']:.2f}% de Hs Trab + Repouso):","","", f"{total_pagamento['sub_total_dois_oito']:.2f}"],
            [f"DIF. DE CALCULA SEM ANTERIOR (+):","","", f"{total_pagamento['sub_total_dois_treze']:.2f}"],
            [f"COREÇÃO (+) :","","", f"{total_pagamento['sub_total_dois_nove']:.2f}"],
            [f"CORREÇÃO (-):","","", f"{total_pagamento['sub_total_dois_dez']:.2f}"],
            [f"PARC. DE ADIANTAMENTO SALARIAL (-):","","", f"{total_pagamento['sub_total_dois_onze']:.2f}"],
            [f"SALDO A RECEBER:","","", f"{total_pagamento['sub_total_tres']:.2f}"],
            ["Obs: Comunicamos que providencie sua documentação completa para a realização do exame adimissional (ASO) e", "",""],
            ["Registro Legal  na Empresa.", "", ""]
            
        ]

    def _create_table(self, content):
        table = Table(content)
        table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Alinhamento à esquerda
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'), # Alinhamento à direita para a segunda coluna
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), # Fonte
                    ('FONTSIZE', (0, 0), (-1, -1), 11), # Tamanho da fonte
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding na parte inferior do cabeçalho   
                    ('FONTSIZE', (0, -1), (-1, -1), 11),  # Tamanho da fonte para a última linha
                    ('FONTSIZE', (0, 20), (-1, 20), 11),  # Tamanho da fonte para a linha 20 (índice 19)
                    ('FONTSIZE', (0, 21), (-1, 22), 11),  # Tamanho da fonte para a linha 21 (índice 21)
                    ('ALIGN', (0, 21), (-1, 21), 'LEFT'),  # Alinhamento à esquerda para a linha 20
                    ('SPAN', (0,21), (3, 21)),  # Faz com que a linha 20 ocupe as quatro colunas
                    # Negrito para "SUB-TOTAL 1" e "SUB-TOTAL 2" e a primeira Linha
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrito para 1 linhas'
                    ('FONTNAME', (0, 12), (-1, 12), 'Helvetica-Bold'), # Negrito para "SUB-TOTAL 2"
                    ('FONTNAME', (0, 7), (-1, 7), 'Helvetica-Bold'),  # Negrito para "SUB-TOTAL 1"
                    ('FONTNAME', (0, 20), (-1, 20), 'Helvetica-Bold') # Negrito para "SUB-TOTAL 3"
                
                    
                    
                ]))
            
        return table

    def _draw_footer(self, elements):

        data_pagamento = self.funcao.data_pagamento.strftime("%d/%m/%Y")
        
        footer = [
            [f"ANANINDEUA. {data_pagamento}","",""],
            ["_______________________________________________________", "", ""],
            [self.funcao.funcionario['nome_funcionario'] + f"- {self.funcao.nome_cargo}", ""],
            [f"CPF: {self.funcao.funcionario['numero_cpf']}","",""],
            [f"CHAVE PIX: {self.funcao.funcionario['chave_pix']}","",""],
        ]
        footer_table = Table(footer)
        footer_table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                          ('FONTSIZE', (0, 0), (-1, -1), 14)]))
        elements.append(footer_table)