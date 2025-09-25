from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm
from io import BytesIO
from gerar_sub_total_um_reembolso import Sub_total_um_reembolso
from openpyxl import Workbook
from openpyxl import Workbook, load_workbook
import os
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from pymongo import MongoClient
from bson import ObjectId
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from salvar_dados_mongo import MongoDBHandler  # Importe a classe MongoDBHandler
import logging


# Configuração básica de logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class Gerar_olerite_reembolso:
    def __init__(self, funcao):
        self.funcao = funcao
        self.margin = 20  # Margens em mm
        self.page_width, self.page_height = A4  
        self.mongo_handler = MongoDBHandler('FUNCIONARIOS_VR3_PAGAMENTOS', 'pagamento_reembolso')  # Inicializa o handler do MongoDB
        logging.info("Classe Gerar_olerite_reembolso inicializada com sucesso.")

   

    def converter_datas(dado):
        for key, value in dado.items():
            if isinstance(value, datetime.date):  # Verifica se o valor é do tipo datetime.date
                dado[key] = datetime.combine(value, datetime.min.time())  # Converte para datetime.datetime
        return dado


    def gerar_sub_um_reembolso(self):
        logging.info("Iniciando geração do PDF.")
        try:
            # Calcular pagamento
            total_pagamento = Sub_total_um_reembolso.calcular_pagamento_um_reembolso(self.funcao)
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
                "nome": self.funcao.funcionario_reembolso['nome_funcionario'],
                "equipe": self.funcao.funcionario_reembolso['equipe'],
                "funcao": self.funcao.funcionario_reembolso['nome_funcao'],
                "empresa": self.funcao.funcionario_reembolso['empresa'],
                "cnpj_empresa": self.funcao.funcionario_reembolso['cnpj_empresa'],
                "cpf": self.funcao.funcionario_reembolso['numero_cpf'],
                "chave_pix": self.funcao.funcionario_reembolso['chave_pix'],
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
        total_pagamento = self.funcao.calcular_pagamento_um_reembolso()

        valor_sub_total_tres = total_pagamento.get('sub_total_tres')
      
        

        header = [
            [self.funcao.funcionario_reembolso['empresa'], "", ""],
            [f"CNPJ:{self.funcao.funcionario_reembolso['cnpj_empresa']}", "", ""],
            ["", "", ""],   
            ["R   E   C   I   B   O","", ""],
            ["", "", ""],
            [f"RECEBI DE {self.funcao.funcionario_reembolso['empresa']} A QUANTIA DE R$: {total_pagamento['sub_total_tres']:.2f}","",""],
            ["", "", ""],
            
        ]


        header_table = Table(header, colWidths=[250, 100, 150])
        header_table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                            ('ALIGN', (0, 0), (0, 1), 'LEFT'),   # empresa e CNPJ
                                            ('ALIGN', (0, 3), (2, 3), 'CENTER'), # RECIBO centralizado
                                            ('ALIGN', (0, 5), (0, 5), 'LEFT'),   # RECEBI DE... alinhado à esquerda

                                            # Fonte e espaçamentos
                                            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                            ('FONTSIZE', (0, 0), (-1, -1), 14),
                                            ('LEFTPADDING', (0, 0), (-1, -1), -20),
                                            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
                                            ('TOPPADDING', (0, 0), (-1, -1), 10),
                                            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),

                                            # "RECIBO" ocupando 3 colunas
                                            ('SPAN', (0, 3), (2, 3)),
                                           ]))
        

        elements.append(header_table)

    def _prepare_content(self, total_pagamento):
        styles = getSampleStyleSheet()
        normal = styles['Normal']

        # formata valor para padrão brasileiro
        salario_formatado = f"{self.funcao.funcionario_reembolso['salario_base']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        salario_paragraph = Paragraph(
            "S&nbsp;A&nbsp;L&nbsp;A&nbsp;R&nbsp;I&nbsp;O&nbsp;&nbsp;&nbsp;B&nbsp;A&nbsp;S&nbsp;E&nbsp;&nbsp;<b>R$ {}</b>".format(salario_formatado),
            normal
        )


        data_inicio_formatada = (self.funcao.data_inicio).strftime('%d/%m/%Y') 
        data_fim_formatada = (self.funcao.data_fim).strftime('%d/%m/%Y')

        return [
            [f"REFERÊNCIA: HORAS EXTRAS E ADICIONAL NOTURNO", f"{data_inicio_formatada}","Até", f"{data_fim_formatada}"],
            [salario_paragraph, "", "", ""],
            [f"NOME: {self.funcao.funcionario_reembolso['nome_funcionario']}", "    QUAT.  VL R$","","PROVENTO"],
            [f"HORAS EXTRAS DE 50%:", f"{self.funcao.horas_extras_um:.2f}  X  {self.funcao.funcionario_reembolso['valor_hora_extra_um']:.2f}","=", f"{total_pagamento['pagamento_horas_extras_um']:.2f}"],
            [f"HORAS EXTRAS DE 100%:", f"{self.funcao.horas_extras_dois:.2f}  X  {self.funcao.funcionario_reembolso['valor_hora_extra_dois']:.2f}","=", f"{total_pagamento['pagamento_horas_extras_dois']:.2f}"],
            [f"ADICIONAL NOTURNO:", f"{self.funcao.horas_noturnas:.2f}  X  {self.funcao.funcionario_reembolso['adicional_noturno']:.2f}","=", f"{total_pagamento['pagamento_adicional_noturno']:.2f}"],
            [f"SALDO A RECEBER:","","", f"{total_pagamento['sub_total_tres']:.2f}"],
            ["", "", "", ""],  # Linha em branco para espaçamento
            ["", "", "", ""],  # Linha em branco para espaçamento   
            
        ]

    def _create_table(self, content):
        table = Table(content)
        table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Alinhamento à esquerda
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'), # Alinhamento à direita para a segunda coluna
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), # Fonte
                    ('FONTSIZE', (0, 0), (-1, -1), 11), # Tamanho da fonte
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding na parte inferior do cabeçalho   s
                    ('SPAN', (0,21), (3, 21)),  # Faz com que a linha 20 ocupe as quatro colunas
                    # Negrito para "SUB-TOTAL 1" e "SUB-TOTAL 2" e a primeira Linha
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrito para 1 linhas'
                    ('FONTNAME', (0, 6), (-1, 6), 'Helvetica-Bold'),  # Negrito para "SUB-TOTAL 1"
                
                    
                    
                ]))
            
        return table

    def _draw_footer(self, elements):

        data_pagamento = self.funcao.data_pagamento.strftime("%d/%m/%Y")
        
        footer = [
            [f"ANANINDEUA. {data_pagamento}","",""],
            ["", "", "", ""],  # Linha em branco para espaçamento
            ["", "", "", ""],  # Linha em branco para espaçamento   
            ["______________________________________________________________", "", ""],
            [self.funcao.funcionario_reembolso['nome_funcionario'] + f"- {self.funcao.nome_cargo}", ""],
            [f"CPF: {self.funcao.funcionario_reembolso['numero_cpf']}","",""],
            ["VALOR EM R$","",""],
        ]
        footer_table = Table(footer)
        footer_table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                          ('FONTSIZE', (0, 0), (-1, -1), 12)])),
        elements.append(footer_table)