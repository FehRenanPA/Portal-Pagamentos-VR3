from flask import Flask, request, jsonify, render_template, send_file, abort
from datetime import datetime
from gerar_sub_total_um import Sub_total_um
from gerador_olerite import Gerar_olerite
from criar_cargo import CriarFuncionario
import json
import os
import time
from flask_cors import CORS
import logging
import uuid
import sys
from werkzeug.serving import run_simple
from io import BytesIO
from docx.shared import Pt
from docx.shared import Pt, Cm
from io import BytesIO
import threading
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configuração do logging
logging.basicConfig(level=logging.DEBUG,  # Exibe logs de nível DEBUG e superiores
                    format='%(asctime)s - %(levelname)s - %(message)s')


class CriarFuncionario:
    

        @app.route('/api/funcionarios', methods=['GET'])
        def get_all_funcionarios():
            """Retorna todos os funcionários."""
            return jsonify(funcionario_dict), 200
        #Carregar dados cadastrados na tabela no front
        @staticmethod
        def carregar_funcionarios():
            """Carrega os cargos do arquivo JSON."""
            if os.path.exists('funcionario.json'):
                with open('funcionario.json', 'r') as file:
                    try:
                        return json.load(file)
                    except json.JSONDecodeError:
                        # Em caso de erro no arquivo JSON, retorna um dicionário vazio.
                        print("Erro ao ler o arquivo funcionario.json. O arquivo está corrompido.")
                        return {}
            return {}

        @staticmethod
        def salvar_cargos(funcionario_dict):
                    """Salva os cargos no arquivo JSON."""
                    with open('funcionario.json', 'w') as file:
                        json.dump(funcionario_dict, file, indent=4)  # Adiciona indentação para legibilidade.
    # Carrega cargos inicialmente
funcionario_dict = CriarFuncionario.carregar_funcionarios()    

#Reencia o servidor após cada evento
def reiniciar_servidor():
    """ Reinicia o servidor Flask para aplicar alterações no dicionário """
    os.execv(sys.executable, ['python'] + sys.argv)
    
@app.after_request
def after_request(response):
    # Verifica se a resposta não é None
    if response is None:
        return '', 204  # Retorna uma resposta vazia com status 204 No Content

    # Se for uma resposta válida, continue com a lógica
    if request.method in ['POST', 'PUT']:
        app.logger.info('Atualização detectada, aplicando reload.')
        threading.Timer(1, reiniciar_servidor).start()
        # Lógica de reload do dicionário se aplicável
    
    return response



##----------------------------------> Gerar etiquetas <------------------------------------##

@app.route('/api/gerar-etiquetas', methods=['POST'])
def gerar_etiquetas():
    data = request.get_json()
    data_inicio = datetime.strptime(data.get("data_inicio"), "%Y-%m-%d").strftime("%d/%m")
    data_fim = datetime.strptime(data.get("data_fim"), "%Y-%m-%d").strftime("%d/%m/%Y")

    # Carregar o dicionário de funcionários
    funcionario_dict = CriarFuncionario.carregar_funcionarios()
    if not funcionario_dict:
        return jsonify({"error": "Nenhum funcionário encontrado"}), 404
    

    # Ordenar os funcionários por nome em ordem alfabética
    funcionarios_ordenados = sorted(funcionario_dict.values(), key=lambda f: f.get("nome_funcionario", ""))

    # Configurações básicas da página e das etiquetas
    page_width = 595  # Largura da página A4 em pontos
    page_height = 842  # Altura da página A4 em pontos
    etiqueta_largura = page_width / 2 - 30  # Largura de cada etiqueta (2 colunas)
    etiqueta_altura = 70  # Altura de cada etiqueta
    margem_superior = page_height - 45
    margem_lateral = 3.5
    max_linhas_por_pagina = 11  # Máximo de linhas por página

    # Preparação para o PDF
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=(page_width, page_height))
    linha_atual = 0
    col_atual = 0
    y = margem_superior

    # Itera sobre os funcionários ordenados para criar as etiquetas
    for funcionario in funcionarios_ordenados:
        nome_funcao = funcionario.get("nome_funcao","Função Não Informada")
        if nome_funcao == "INATIVO":
           continue  # 
       
        nome_funcionario = funcionario.get("nome_funcionario", funcionario.get("numero_cpf", "Nome não disponível"))
        equipe = funcionario.get("equipe", "Equipe Não Cadastrada")
        etiqueta_texto = f"{""}\n{nome_funcionario}\n{nome_funcao}\n{data_inicio} á {data_fim}"

        # Avança para uma nova página se o limite de linhas for atingido
        if linha_atual >= max_linhas_por_pagina:
            c.showPage()
            c.setFont("Helvetica", 1)
            y = margem_superior
            linha_atual = 0
            col_atual = 0

        # Posicionamento da etiqueta
        x_dados = margem_lateral + (col_atual * etiqueta_largura)
        c.setFont("Helvetica", 10)
        linha_y = y - 5
        for linha in etiqueta_texto.split('\n'):
            c.drawCentredString(x_dados + etiqueta_largura / 2, linha_y, linha)
            linha_y -= 10

        # Alterna entre colunas e ajusta linhas
        col_atual = (col_atual + 1) % 2
        if col_atual == 0:
            y -= etiqueta_altura
            linha_atual += 1

    # Salvar o PDF e enviar o conteúdo
    c.save()
    output.seek(0)
    return output.getvalue(), 200, {'Content-Type': 'application/pdf', 'Content-Disposition': 'attachment; filename="etiquetas.pdf"'}



##----------------------------------> API de Funcionarios <-----------------------------------##
@app.route('/api/funcionarios', methods=['GET', 'POST'])
def funcionarios():
#print("Requisição recebida")  # Log da requisição
    
    if request.method == 'POST':
            data = request.json
            if not data:  # Verifica se data é None ou um dicionário vazio
                print("Dados não recebidos corretamente!")
                return jsonify({"message": "Dados não recebidos corretamente!"}), 400
            
            print(f"Dados recebidos: {data}")

            # Validação dos campos obrigatórios
            required_fields = [
                'nome_funcionario',
                'numero_cpf',
                'chave_pix',
                'valor_hora_base',
                'valor_hora_extra_um',
                'valor_hora_extra_dois',
                'repouso_remunerado',
                'adicional_noturno',
                'desconto_inss',
                'desconto_refeicao',
                'desconto_transporte',
                'pagamento_fgts',
                'valor_decimo_terceiro',
                'valor_ferias',
                'valor_um_terco_ferias'
                
            ]

            # Verifica se todos os campos obrigatórios estão presentes
            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields: 
                print(f"Campos obrigatórios faltando: {missing_fields}")
                return jsonify({"message": f"Campos obrigatórios faltando: {', '.join(missing_fields)}!"}), 400
            
            # Converte os valores para float
            for field in required_fields[1:]:  # Ignora o primeiro campo 'nome_funcionario'
                if field in data:
                   if field in ['numero_cpf', 'chave_pix']:  # Esses campos devem ser string
                        data[field] = str(data[field])
                
                else:
                     
                  try:
                        data[field] = float(data[field])
                  except ValueError:
                        return jsonify({"message": f"Valor inválido para {field}!"}), 400
            
            # Remover espaços em branco e validar nome Funcionario
            nome = data['nome_funcionario'].strip()
            if not nome:
                return jsonify({"message": "O campo nome_funcionario não pode estar vazio!"}), 400
            
            print(f"Nome do Funcionario: '{nome}'")  # Log para verificar o valor de nome_cargo
            

##----------------------------------> Criar cadastro do funcionario <-----------------------------------##
@app.route('/api/criar_funcionario', methods=['POST'])
def criar_funcionario():
    try:
        data = request.json
        app.logger.info(f"Dados recebidos para criação de funcionário: {data}")

        required_fields = ['nome_funcionario', 'nome_funcao','equipe','numero_cpf', 'chave_pix', 'valor_hora_base', 
                           'valor_hora_extra_um', 'valor_hora_extra_dois', 'adicional_noturno', 
                           'repouso_remunerado', 'valor_ferias', 'valor_um_terco_ferias', 
                           'valor_decimo_terceiro', 'pagamento_fgts', 'desconto_inss', 
                           'desconto_refeicao', 'desconto_transporte']

        if not data or any(field not in data for field in required_fields):
            return jsonify({'error': 'Dados obrigatórios faltando!'}), 400

        ## Verificação de duplicidade pelo CPF para garantir que não exista já um funcionário com o mesmo CPF
        if any(func['numero_cpf'] == data['numero_cpf'] for func in funcionario_dict.values()):
            return jsonify({'error': 'Funcionário com esse CPF já existe!'}), 409

        # Gera um ID único para o novo funcionário
        funcionario_id = str(uuid.uuid4())
        while funcionario_id in funcionario_dict:
            funcionario_id = str(uuid.uuid4())  # Gera novamente se já existe

        # Adiciona o novo funcionário ao dicionário com o ID como chave
        funcionario_dict[funcionario_id] = {
            'nome_funcionario': data['nome_funcionario'],
            'nome_funcao': data['nome_funcao'],
            'equipe':data['equipe'],
            'numero_cpf': data['numero_cpf'],
            'chave_pix': data['chave_pix'],
            'valor_hora_base': data['valor_hora_base'],
            'valor_hora_extra_um': data['valor_hora_extra_um'],
            'valor_hora_extra_dois': data['valor_hora_extra_dois'],
            'adicional_noturno': data['adicional_noturno'],
            'repouso_remunerado': data['repouso_remunerado'],
            'valor_ferias': data['valor_ferias'],
            'valor_um_terco_ferias': data['valor_um_terco_ferias'],
            'valor_decimo_terceiro': data['valor_decimo_terceiro'],
            'pagamento_fgts': data['pagamento_fgts'],
            'desconto_inss': data['desconto_inss'],
            'desconto_refeicao': data['desconto_refeicao'],
            'desconto_transporte': data['desconto_transporte']
        }

        # Salva os dados atualizados no arquivo JSON
        CriarFuncionario.salvar_cargos(funcionario_dict)
          
        app.logger.info(f'Funcionário {data["nome_funcionario"]} criado com sucesso com ID: {funcionario_id}.')
        return jsonify({'message': 'Funcionário criado com sucesso!', 'data': funcionario_dict[funcionario_id]}), 201

    except Exception as e:
        app.logger.error(f'Erro ao criar funcionário: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor.'}), 500


 
##----------------------------------> Editar cadastro do funcionario <-----------------------------------##
@app.route('/api/funcionario/<string:funcionario_id>', methods=['PUT'])
def editar_funcionario(funcionario_id):
    
    global funcionario_dict 
    logger.debug(f'Tentando atualizar o funcionário com id: {funcionario_id}')

    # Verifica se o ID é nome (antigo) ou uid (novo)
    if funcionario_id not in funcionario_dict:
        logger.warning(f'Funcionário com id {funcionario_id} não encontrado')
        return jsonify({'message': 'Funcionário não encontrado'}), 404

    data = request.json

    # Checa se é um registro antigo sem UID
    if not isinstance(funcionario_id, str) or len(funcionario_id) != 36:
        # Criar um novo UID para o registro
        novo_uid = str(uuid.uuid4())
        funcionario_dict[novo_uid] = funcionario_dict.pop(funcionario_id)
        funcionario_dict[novo_uid]["nome_funcionario"] = funcionario_id  # Mantém o nome como `nome_funcionario`
        funcionario_id = novo_uid  # Atualiza para a nova chave UID
    
    funcionario = funcionario_dict[funcionario_id]
    
    # Verificar se o CPF novo já existe em outro funcionário
    if "numero_cpf" in data:
        cpf_novo = data["numero_cpf"]
        for uid, dados in funcionario_dict.items():
            if uid != funcionario_id and dados.get("numero_cpf") == cpf_novo:
                return jsonify({'message': 'Outro funcionário já possui este CPF.'}), 409
    
    # Verifica e adiciona campo `nome_funcao` se estiver ausente
    funcionario.setdefault('nome_funcao', data.get('nome_funcao', ''))
    funcionario.setdefault('equipe', data.get('equipe', ''))

    # Atualiza os dados com os valores recebidos
    campos = ['nome_funcionario', 'nome_funcao', 'equipe', 'numero_cpf', 'chave_pix', 'valor_hora_base',
              'valor_hora_extra_um', 'valor_hora_extra_dois', 'adicional_noturno', 'repouso_remunerado',
              'valor_ferias', 'valor_um_terco_ferias', 'valor_decimo_terceiro', 'pagamento_fgts', 
              'desconto_inss', 'desconto_refeicao', 'desconto_transporte']
    
    for campo in campos:
        if campo in data:
            funcionario[campo] = data[campo]
    
    CriarFuncionario.salvar_cargos(funcionario_dict)
    
    
    logger.info(f'Funcionário {funcionario_id} atualizado com sucesso: {funcionario}')
    return jsonify({'message': 'Funcionário atualizado com sucesso', 'data': funcionario}), 200
    
    
    
   
###---------------------------------------> Criar Recibo <--------------------------------------------##

@app.route('/api/criar_recibo', methods=['POST'])
def criar_recibo():
    
    
        data = request.json 
        #1 logg
        app.logger.info(f"Dados recebidos pelo back: {data}")


        required_fields = [ 'data_inicio','data_fim', 'data_pagamento','name_funcionario','nome_cargo', 'horas_trabalhadas','valor_diarias', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas', 'correcao_positiva', 'correcao_negativa','parcela_vale']
 
        
        # Verifica se os dados obrigatórios estão presentes
        if not data or any(field not in data for field in required_fields):
            #Loggs
        
            
            return jsonify({'error': 'Dados obrigatórios faltando!'}), 400
        
            # Validação de data
        try:
            data['data_inicio'] = datetime.strptime(data['data_inicio'], '%d-%m-%Y').date()
            data['data_fim'] = datetime.strptime(data['data_fim'], '%d-%m-%Y').date()
            data['data_pagamento'] = datetime.strptime(data['data_pagamento'], '%d-%m-%Y').date()
        except ValueError:
            app.logger.error("Erro na validação das datas.")
            return jsonify({'error': 'Datas devem estar no formato DD-MM-YYYY!'}), 400


        # Converte valores de horas para float
        try:

            for field in ['horas_trabalhadas', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas', 'valor_diarias', 'correcao_positiva', 'correcao_negativa','parcela_vale']:

                data[field] = float(data[field])
        except ValueError as e:
            app.logger.error(f"Erro ao converter valores: {e}")
            return jsonify({'error': 'Valores de horas devem ser numéricos!'}), 400
        
        ##Requeste pare trazer funcioanrios
        
        funcionario_id= data['name_funcionario']
        funcionario = funcionario_dict.get(funcionario_id)

        if not funcionario:
            return jsonify({'error': 'Funcionario não encontrado!'}), 404   

        # Cria o objeto funcionario com base nos dados recebidos
        data = request.get_json()  # Ou request.form se for um form HTML
        print(f"Dados da requisição: {data}")
        
        if funcionario.get('nome_funcao') == "INATIVO":
            
            return jsonify({'error': 'Funcionário está inativo!'}), 403  # Erro 403 indicando que o funcionário está inativo
   
        funcionario = Sub_total_um(data['nome_cargo'], funcionario_id , data['data_inicio'], data['data_fim'], data['data_pagamento'])

        # Adicionando as horas e outros dados   
        
        funcionario.adicionar_horas_trabalhadas(data['horas_trabalhadas'])
        funcionario.adicionar_horas_noturnas(data['horas_noturnas'])
        funcionario.adicionar_horas_extras_um(data['horas_extras_um'])
        funcionario.adicionar_horas_extras_dois(data['horas_extras_dois'])
        funcionario.adicionar_correcao_positiva(data['correcao_positiva']) 
        funcionario.adicionar_correcao_negativa(data['correcao_negativa']) 
        funcionario.adicionar_valor_por_hora(data['valor_diarias'])
        funcionario.adicionar_pagamento_vale(data['parcela_vale'])
        
        
        
        # Gerar o olerite
        olerite = Gerar_olerite(funcionario)
        buffer = olerite.gerar_sub_um()
        
        return send_file(buffer, as_attachment=True, download_name='recibo.pdf', mimetype='application/pdf')



##---------------------------------> Retorna Funcionarios para o Front <-------------------------------##
@app.route('/api/funcionarios/<key>', methods=['GET'])
def get_funcionario(key):
    funcionario = funcionario_dict.get(key)
    
    # Verifica se o funcionário existe
    if funcionario:
        # Define valores padrão para 'nome_funcionario' e 'nome_funcao' se ausentes
        funcionario.setdefault('nome_funcionario', 'Nome não cadastrado')
        funcionario.setdefault('nome_funcao', 'Função não cadastrada')
        return jsonify(funcionario), 200
    
    return jsonify({'error': 'Funcionário não encontrado'}), 404


##----------------------------------> Baixar Excell <-----------------------------------##                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
# Diretório onde os arquivos estão localizados
DIRETORIO_ARQUIVOS = os.path.join(app.root_path, 'static') ##Mudar se necessario


@app.route('/api/listar_arquivos', methods=['GET'])
def listar_arquivos():
    try:
        logging.info("Requisição recebida na rota '/api/listar_arquivos'.")  # Log de entrada da requisição
        arquivos = os.listdir(DIRETORIO_ARQUIVOS)
        # Filtra apenas os arquivos .xlsx
        arquivos_excel = [arq for arq in arquivos if arq.endswith('.xlsx')]
        
        logging.info(f"Arquivos encontrados: {arquivos_excel}")  # Log para exibir os arquivos encontrados
        
        return jsonify({'arquivos': arquivos_excel})
    except Exception as e:
        
        logging.error(f"Erro ao listar arquivos: {str(e)}")  # Log de erro caso ocorra algum problema
        
        return jsonify({'erro': str(e)}), 500

@app.route('/baixar_excel/<arquivo>', methods=['GET'])
def baixar_excel(arquivo):
    # Caminho completo do arquivo
    caminho_arquivo = os.path.join(DIRETORIO_ARQUIVOS, arquivo)

    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        abort(404, "Arquivo não encontrado")

    # Envia o arquivo para download, especificando o tipo de conteúdo
    return send_file(caminho_arquivo, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') 

@app.route('/api/funcionarios/<int:id>', methods=['PUT'])
def update_funcionario(id):
    data = request.get_json()
    # Atualize os dados do funcionário no banco de dados
    return jsonify({'message': 'Funcionário atualizado com sucesso.'})

@app.route('/')
def home():
    return "Home Page"

@app.route('/about')
def about():
    return "About Page"

# Se precisar de um endpoint com o mesmo nome, altere
@app.route('/new-home')
def new_home():
    return "New Home Page"



if __name__ == '__main__':
    #app.run(debug=True, port=5000)
     # Inicia o servidor Flask
    run_simple('127.0.0.1', 5000, app, use_reloader=True)
    
      