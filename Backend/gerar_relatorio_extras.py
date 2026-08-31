from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import datetime
import io

class GerarExcelExtras:
    def __init__(self, data_inicio, data_fim, empresas, documentos):
        """
        Inicializa o gerador de relatórios.

        :param data_inicio: Data de início do relatório (string no formato "dd/mm/yy" ou "dd/mm/yyyy").
        :param data_fim: Data de fim do relatório (string no formato "dd/mm/yy" ou "dd/mm/yyyy").
        :param empresas: Lista de empresas incluídas no relatório.
        :param documentos: Lista de documentos retornados pela API.
        """
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.empresas = empresas
        self.documentos = documentos

    def formatar_cpf(self, cpf):
        """
        Formata o CPF no padrão XXX.XXX.XXX-XX.

        :param cpf: CPF como string ou número.
        :return: CPF formatado ou original se inválido.
        """
        cpf = ''.join(filter(str.isdigit, str(cpf)))  # Remove não numéricos
        if len(cpf) == 11:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        return cpf

    def gerar_excel_em_memoria(self):
        """
        Gera um relatório em formato Excel com os dados do relatório e retorna em memória.

        :return: Arquivo Excel em formato binário.
        """
        try:
            # Criação do workbook e da planilha
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = "Relatório de Pagamentos de Horas Extras"

            # Adiciona cabeçalho do relatório com datas
            self._draw_header(sheet)

            # Adiciona cabeçalhos da tabela
            headers = ["N°", "Nome", "Função", "Empresa","CPF", "Valor Bruto"]
            sheet.append(headers)

            # Aplica estilos ao cabeçalho da tabela
            for cell in sheet[2]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal="center")

            # Adiciona os documentos ao Excel
            for i, doc in enumerate(self.documentos, start=1):
                sheet.append([
                    i,
                    doc.get("nome", ""),
                    doc.get("funcao", ""),
                    doc.get("empresa", ""),
                    self.formatar_cpf(doc.get("cpf", "")),
                    round(doc.get("valor_bruto", 0.0), 2),
                ])

            # Salva o arquivo em memória (BytesIO)
            memoria = io.BytesIO()
            workbook.save(memoria)
            memoria.seek(0)  # Volta o ponteiro para o início do arquivo

            # Retorna o conteúdo do arquivo em memória
            return memoria.getvalue()

        except Exception as e:
            print(f"Erro ao gerar o relatório: {e}")
            return None

    def _draw_header(self, sheet):
        """
        Adiciona o cabeçalho com as datas de início e fim do período.
        """
        # Tenta analisar as datas com ano de 4 dígitos
        try:
            data_inicio_formatada = datetime.datetime.strptime(self.data_inicio, "%d/%m/%y").strftime('%d/%m/%Y')
        except ValueError:
            data_inicio_formatada = datetime.datetime.strptime(self.data_inicio, "%d/%m/%Y").strftime('%d/%m/%Y')

        try:
            data_fim_formatada = datetime.datetime.strptime(self.data_fim, "%d/%m/%y").strftime('%d/%m/%Y')
        except ValueError:
            data_fim_formatada = datetime.datetime.strptime(self.data_fim, "%d/%m/%Y").strftime('%d/%m/%Y')
        
        # Texto do cabeçalho com a data
        header_text = f"Relatórios de Pagamento de Hs Extras. Período: {data_inicio_formatada} até {data_fim_formatada}"

        # Adiciona o cabeçalho à planilha
        sheet.merge_cells('A1:I1')  # Mescla a linha para o cabeçalho
        header_cell = sheet['A1']
        header_cell.value = header_text
        header_cell.font = Font(bold=True, size=14)
        header_cell.alignment = Alignment(horizontal="center")
        sheet.append([])  # Adiciona uma linha em branco para separar o cabeçalho dos dados
