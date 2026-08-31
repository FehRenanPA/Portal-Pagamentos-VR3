import os
os.environ['REPORTLAB_DISABLE_CYTHON'] = 'yes'
from numpy.random import normal
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import mm
from io import BytesIO
from gerar_sub_total_um_ferias import Sub_total_um_ferias
from openpyxl import Workbook
from openpyxl import Workbook, load_workbook
import os
from reportlab.platypus import Paragraph
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter
from pymongo import MongoClient
from bson import ObjectId
from salvar_dados_mongo import MongoDBHandler  # Importe a classe MongoDBHandler
import logging
from datetime import datetime
import os
os.environ['REPORTLAB_DISABLE_CYTHON'] = 'yes'


# Configuração básica de logging
logging.basicConfig(
    level=logging.DEBUG,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

class Gerar_olerite_ferias:
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


    def gerar_sub_um_ferias(self):
        logging.info("Iniciando geração do PDF.")
        try:
            # Calcular pagamento
            total_pagamento = Sub_total_um_ferias.calcular_pagamento_um(self.funcao)
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
                "data_fim": self.funcao.data_fim.strftime('%d/%m/%y'),
                "empresa": self.funcao.empresa_exe,
                  # Adicionando a data e hora atual:
                "data_atualizacao": datetime.now()  # Salva como objeto Date/ISODate do MongoDB
            }
           

            # Inserir no MongoDB
            id_salvo = self.mongo_handler.inserir_ou_atualizar_dado(dados)
            logging.info(f"Dados salvos no MongoDB com ID: {id_salvo}")

            return buffer
        
        except Exception as e:
            logging.error(f"Erro ao ao salvar os dados nos mongoDB: {str(e)}", exc_info=True)
            raise

    #def gerar_sub_um_ferias(self):
        #return self.gerar_sub_um()

    def _draw_header(self, elements):
        total_pagamento = self.funcao.calcular_pagamento_um()

        # formata valor para padrão brasileiro
        
  
        valor_sub_total_tres = total_pagamento.get('sub_total_tres')
        empresa_exe = self.funcao.empresa_exe

        cnpj = "45.528.735/0001-20" if empresa_exe == "VR LTA" else "12.507.345/0001-15"

        header = [
            [f"{empresa_exe}", "", ""],
            [f"CNPJ: {cnpj}", "", ""], #Data
            ["", "", ""],   
            ["", "", ""],
            ["","R   E   C   I   B   O", ""],
            ["", "", ""],
            ["",""*20, f"VALOR: R$ {total_pagamento['sub_total_bruto']:.2f}"],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],

            [f"RECEBI DE {empresa_exe} A QUANTIA DE R$: {total_pagamento['sub_total_bruto']:.2f}","",""],

            ["", "", ""]
                
        ]


        header_table = Table(header, hAlign='LEFT',colWidths=[250, 100, 150])
        header_table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                          ('ALIGN', (1, 4), (1, 4), 'CENTER'), # RECIBO centralizado
                                           ('ALIGN', (1, 0), (1, 0), 'CENTER'),
                                           ('ALIGN', (4, 0), (4, 0), 'LEFT'), 
                                           ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                           ('SPAN', (0, 9), (2, 9)),
                                           ('ALIGN', (0, 9), (2, 9), 'CENTER'),
                                           ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                           ('FONTSIZE', (0, 0), (-1, -1), 14)]))
        

        elements.append(header_table)

    def _prepare_content(self, total_pagamento):
        faltas = f" {total_pagamento.get('faltas', 0):.2f}"
        faltas_d_s_r = f" {total_pagamento.get('faltas_d_s_r', 0):.2f}"
        d_s_r_adicionais = f"{total_pagamento.get('d_s_r_adicionais', 0):.2f}"
        d_s_r = f" {total_pagamento.get('d_s_r', 0):.2f}"
        salario_formatado = f" {total_pagamento.get('salario_base_mes', 0):.2f}"
            
        data_inicio_formatada = (self.funcao.data_inicio).strftime('%d/%m/%Y') 
        data_fim_formatada = (self.funcao.data_fim).strftime('%d/%m/%Y')

        return [
            [f"PROVENTOS DE PRESTAÇÃO DE SERVIÇOS NO PERÍODO DE", f"{data_inicio_formatada}","Até", f"{data_fim_formatada}"],
            [f"SALARIO BASE :   R${salario_formatado}", "", "", ""],
            [f"NOME: {self.funcao.funcionario['nome_funcionario']}", "    QUAT.  VL R$","","PROVENTO"],
            [f"HORAS TRABALHADAS:", f"{self.funcao.horas_trabalhadas:.2f}  X  {self.funcao.funcionario['valor_hora_base']:.2f}","=", f"R${total_pagamento['pagamento_base']:.2f}"],
            [f"REPOUSO REMUNERADO:", f"{self.funcao.repouso_remunerado:.2f}  X  {self.funcao.funcionario['repouso_remunerado']:.2f}","=", f"R${total_pagamento['pagamento_folga_remunerada']:.2f}"],
            [f"HORAS EXTRAS DE 50%:", f"{self.funcao.horas_extras_um:.2f}  X  {self.funcao.funcionario['valor_hora_extra_um']:.2f}","=", f"R${total_pagamento['pagamento_horas_extras_um']:.2f}"],
            [f"HORAS EXTRAS DE 100%:", f"{self.funcao.horas_extras_dois:.2f}  X  {self.funcao.funcionario['valor_hora_extra_dois']:.2f}","=", f"R${total_pagamento['pagamento_horas_extras_dois']:.2f}"],
            [f"ADICIONAL NOTURNO:", f"{self.funcao.horas_noturnas:.2f}  X  {self.funcao.funcionario['adicional_noturno']:.2f}","=", f"R${total_pagamento['pagamento_adicional_noturno']:.2f}"],
            [f"D.S.R | ADICIONAIS*:", f"{d_s_r} DIAS","",f"R${d_s_r_adicionais}"],
            [f"SUB-TOTAL:","","", f"{total_pagamento['sub_total_um']:.2f}",],
            [f"DESC. REFEIÇÃO ({self.funcao.funcionario['desconto_refeicao']:.2f}% de Hs Trab + Repouso):","","", f"R${total_pagamento['sub_total_dois']:.2f}"],
            [f"DESC.TRANSPORTE ({self.funcao.funcionario['desconto_transporte']:.2f}% de Hs Trab + Repouso):","","", f"R${total_pagamento['sub_total_tres']:.2f}"],
            [f"FALTAS D.S.R (-):",f"{faltas}","", f"R${faltas_d_s_r}"],
            [f"ADIANTAMENTO SALARIAL (-):","","", f"R${total_pagamento['sub_total_quatro']:.2f}"],
            [f"SALDO A RECEBER:","","", f"R${total_pagamento['sub_total_bruto']:.2f}"],
            
            
        ]

    def _create_table(self, content):
        table = Table(content)
        table.setStyle(TableStyle([
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'), # Alinhamento à esquerda
                    ('ALIGN', (1, 0), (-1, -1), 'RIGHT'), # Alinhamento à direita para a segunda coluna
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'), # Fonte
                    ('FONTSIZE', (0, 0), (-1, -1), 11), # Tamanho da fonte
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Padding na parte inferior do cabeçalho   
                    ('FONTSIZE', (0, -1), (-1, -1), 11),  # Tamanho da fonte para a última linha
                    ('FONTSIZE', (0, 20), (-1, 20), 11),  # Tamanho da fonte para a linha 20 (índice 19)
                    ('FONTSIZE', (0, 21), (-1, 22), 11),  # Tamanho da fonte para a linha 21 (índice 21)
                    ('ALIGN', (0, 21), (-1, 21), 'LEFT'),  # Alinhamento à esquerda para a linha 20
                    ('SPAN', (0,21), (3, 21)),  # Faz com que a linha 20 ocupe as quatro colunas
                    # Negrito para "SUB-TOTAL 1" e "SUB-TOTAL 2" e a primeira Linha
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Negrito para 1 linhas'
                    ('FONTNAME', (0, 14), (-1, 14), 'Helvetica-Bold'), # Negrito para "SALDO A RECEBER"
                    ('FONTNAME', (0, 9), (-1, 9), 'Helvetica-Bold'),  # Negrito para "SUB-TOTAL"
                
                    
                    
                ]))
            
        return table

    def _draw_footer(self, elements):
        cpf_bruto = self.funcao.funcionario['numero_cpf']
        if cpf_bruto and len(cpf_bruto) == 11 and cpf_bruto.isdigit():
            cpf_formatado = f"{cpf_bruto[:3]}.{cpf_bruto[3:6]}.{cpf_bruto[6:9]}-{cpf_bruto[9:]}"
        else:
        # Mantém o CPF bruto ou coloca uma mensagem de erro se a formatação falhar
            cpf_formatado = cpf_bruto


        data_pagamento = self.funcao.data_pagamento.strftime("%d/%m/%Y")
        
        footer = [
            [f"ANANINDEUA. {data_pagamento}","",""],
            ["_______________________________________________________", "", ""],
            [self.funcao.funcionario['nome_funcionario'] + f"- {self.funcao.nome_cargo}", ""],
            [f"CPF: {cpf_formatado}","",""],
            [f"CHAVE PIX: {self.funcao.funcionario['chave_pix']}","",""],
        ]
        footer_table = Table(footer)
        footer_table.setStyle(TableStyle([('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                                          ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                          ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
                                          ('FONTSIZE', (0, 0), (-1, -1), 14)]))
        elements.append(footer_table)