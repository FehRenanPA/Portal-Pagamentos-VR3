from flask import Flask, request, jsonify, render_template, send_file, abort, Response
from datetime import datetime
from criar_cargo import CriarFuncionario
from gerar_sub_total_um import Sub_total_um
from gerador_olerite import Gerar_olerite
import firebase_admin
from firebase_admin import storage, credentials, firestore, auth
from bson.objectid import ObjectId
from pymongo import MongoClient
import json
import os
import time
from flask_cors import CORS
import logging
from utils import is_valid_uuid
import sys
from werkzeug.serving import run_simple
from io import BytesIO
from docx.shared import Pt, Cm
from io import BytesIO
import threading
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from salvar_dados_mongo import MongoDBHandler
from dotenv import load_dotenv
from datetime import datetime
from bson import ObjectId
from pymongo.errors import PyMongoError
from gerar_relatorio import GerarExcel
import traceback
import pyrebase
from firebase_auth import gerar_id_token 
import requests

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

logging.basicConfig(
    level=logging.WARNING,  # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

    
cred_path = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY'),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
    "universe_domain": os.getenv('FIREBASE_UNIVERSE_DOMAIN')
}    
print(cred_path)

cred = credentials.Certificate(cred_path) 
print(f"Service Account Email: {cred.service_account_email}")  
firebase_admin.initialize_app(cred)
firestore_client = firestore.client()  # Inicializa o Firestore
print(f"Service Account Email: {cred.service_account_email}")
app = Flask(__name__)

# Habilitarr CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})


MONGO_URI = os.getenv('MONGO_URI') 


if not MONGO_URI:
    logger.error("A configuração MONGO_URI não foi definida no Firebase Functions ou no arquivo .env!")
    raise ValueError("A configuração MONGO_URI não foi definida!")

client = MongoClient(MONGO_URI)
db = client['FUNCIONARIOS_VR3_PAGAMENTOS']
colecao = db['funcionario']


def gerar_custom_token(uid):
    try:
        if not uid:
            logger.error("UID está vazio!")
            return None
        logger.info(f"Gerando custom token para o UID: {uid}")
        custom_token_str = auth.create_custom_token(uid)

        # Converter o token gerado de bytes para string
        custom_token= custom_token_str.decode('utf-8')

        logger.info(f"Custom token gerado com sucesso para o UID: {uid}")
        return custom_token # Retorne o token como string
    except Exception as e:
        logger.error(f"Erro ao gerar o custom token: {e}")
        return None


def get_id_token(custom_token):
    try:
        # O custom_token é verificado e o ID Token é extraído
        decoded_token = auth.verify_id_token(custom_token)
        return decoded_token['uid']  # Retorna o UID (ou o id_token se for necessário para autenticação)
    except Exception as e:
        logger.error(f"Erro ao verificar o custom_token: {e}")
        return None
   
@app.route('/api/generate-custom-token', methods=['POST'])
def generate_custom_token():
    data = request.get_json()  # Obtém os dados JSON enviados
    logger.debug(f"Dados recebidos: {data}")  # Adicione um log para debugar
    uid = data.get('uid')  # Tenta pegar o 'uid' do corpo da requisição
    if not uid:
        logger.error("UID não fornecido no corpo da requisição")
        return jsonify({"error": "UID não fornecido"}), 400  # Retorna erro se não encontrar o UID
    
    try:
        custom_token = gerar_custom_token(uid)  # Passa o 'uid' para a função
        if custom_token:
            return jsonify({"custom_token": custom_token}), 200
        else:
            return jsonify({"error": "Erro ao gerar custom token"}), 500
    except Exception as e:
        logger.error(f"Erro ao gerar custom token: {str(e)}")
        return jsonify({"error": str(e)}), 500


# Rota para obter dados do Firestore usando o ID Token
@app.route('/api/firestore/get-data', methods=['POST'])
def get_data():
    try:
        data = request.get_json()
        id_token = data.get('id_token')

        # Verifique se o ID Token foi enviado
        if not id_token:
            return jsonify({"error": "ID Token não fornecido"}), 400

        # Valide o ID Token
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')

        return jsonify({"message": "Token válido", "uid": uid}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Rota para gerar e retornar o ID Token - teste
@app.route('/api/auth/get-id-token', methods=['POST'])
def generate_id_token():
    try:
        # Chama a função gerar_id_token
        id_token = gerar_id_token()

        if not id_token:
            return jsonify({"error": "Falha ao gerar o ID Token"}), 500

        return jsonify({"id_token": id_token, "message": "ID Token gerado com sucesso"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/funcionarios', methods=['GET'])
def get_all_funcionarios():
    """Retorna todos os funcionários do MongoDB."""
    funcionarios = CriarFuncionario.carregar_funcionarios()
    return jsonify(funcionarios), 200  # jsonify aplicado aqui, dentro da rota
 


    
####--------------Retorna O funcioanriod e acordo com o ID--------------#####
@app.route('/api/funcionarios/<string:funcionario_id>', methods=['GET'])
def get_funcionario_por_id(funcionario_id):
    """Retorna um único funcionário com base no ID."""
    try:
        print(f"Buscando funcionário com ID: {funcionario_id}")
        funcionario = CriarFuncionario.carregar_funcionario_por_id(funcionario_id)
        if not funcionario:
            return jsonify({'error': 'Funcionário não encontrado'}), 404
        return jsonify(funcionario), 200
    except Exception as e:
        print(f"Erro ao buscar funcionário: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500
    
    

            ######## Preparativos para o Relatorio #########
#---------------- Instancia o manipulador do MongoDB ----------------------------
db_handler = MongoDBHandler(database_name="FUNCIONARIOS_VR3_PAGAMENTOS", collection_name="pagamentos_periodo")

#-------------- Converste o retorno do mongo para string ----------------------
def serialize_document(doc):
    """
    Converte um documento MongoDB para um formato serializável pelo JSON.
    """
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            doc[key] = str(value)  # Converte ObjectId para string
        elif isinstance(value, datetime):
            doc[key] = value.strftime("%Y-%m-%d %H:%M:%S")  # Formata datetime como string
    return doc



class CriarFuncionario:
    
    @staticmethod
    def carregar_funcionario_por_id(funcionario_id):
        """Carrega um funcionário específico pelo ID."""
        try:
            # Verifica se o id é uma string e tenta convertê-lo para ObjectId
            if isinstance(funcionario_id, str):
                funcionario_id = ObjectId(funcionario_id)

            funcionario = colecao.find_one({"_id": funcionario_id})
            if funcionario:
                funcionario['_id'] = str(funcionario['_id'])  # Converte o _id para string
            return funcionario
        except Exception as e:
            print(f"Erro ao carregar funcionário por ID: {e}")
            return None


    
    @staticmethod
    def carregar_funcionarios():
        """Carrega os funcionários diretamente do MongoDB."""
        funcionarios = []
        for funcionario in colecao.find():  # Carregar todos os funcionários do MongoDB
            funcionario['_id'] = str(funcionario['_id'])  # Converte o _id para string
            funcionarios.append(funcionario)
        return funcionarios
    
    @staticmethod
    def salvar_funcionarios(funcionario_dict):
        """Salva os funcionários no MongoDB."""
        # Converte o dicionário de funcionários para uma lista de documentos
        funcionarios_lista = []
        for funcionario_id, dados in funcionario_dict.items():
            funcionario_dados = dados.copy()  # Faz uma cópia para evitar modificações diretas
            funcionario_dados['_id'] = funcionario_id  # Coloca o nome como campo
            funcionarios_lista.append(funcionario_dados)

        # Apaga todos os documentos antes de inserir novos
        #colecao.delete_many({})  # Se quiser substituir todos os documentos, delete os anteriores
        colecao.insert_many(funcionarios_lista)  # Insere novos dados
        print("Funcionários salvos no MongoDB com sucesso.")

funcionario_dict = CriarFuncionario.carregar_funcionarios()
if funcionario_dict:
    print("Funcionários carregados com sucesso:")
else:
    print("Nenhum funcionário encontrado no MongoDB.")


###-----------------Busca dados para gerar o Relatorio/Excell com dados do Mongo--------------------------#####

                   # Listagem geral 

@app.route('/api/listar_documentos', methods=['GET'])
def listar_documentos():
    try:
        # Obtém os parâmetros de data do front-end
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')

        # Validação dos parâmetros obrigatórios
        if not data_inicio or not data_fim:
            logger.warning("Parâmetros obrigatórios ausentes.")
            return jsonify({"erro": "Os parâmetros 'data_inicio' e 'data_fim' são obrigatórios."}), 400

        logger.info(f"Recebendo solicitação para listar documentos entre {data_inicio} e {data_fim}.")

        # Busca os documentos com base no intervalo de datas
        try:
            documentos = db_handler.buscar_dado(data_inicio=data_inicio, data_fim=data_fim)
        except Exception as e:
            logger.error(f"Erro ao buscar documentos no banco de dados: {e}", exc_info=True)
            return jsonify({"erro": "Erro ao buscar documentos no banco de dados."}), 500

        if not documentos:
            logger.info(f"Nenhum documento encontrado entre {data_inicio} e {data_fim}.")
            return jsonify({"mensagem": "Nenhum documento encontrado para o intervalo especificado."}), 404

        # Serializa os documentos encontrados
        documentos_serializados = [serialize_document(doc) for doc in documentos]

        logger.info(f"Documentos encontrados: {len(documentos_serializados)} documentos.")
        return jsonify(documentos_serializados), 200

    except Exception as e:
        logger.error(f"Erro inesperado ao listar documentos: {e}", exc_info=True)
        return jsonify({"erro": "Erro inesperado ao listar documentos"}), 500

    

#-------- Listagem Especifica e gerar arquivo excell
@app.route('/api/relatorio_periodo', methods=['POST'])
def relatorio_periodo():
    try:
        # Obtém o corpo da requisição em JSON
        data = request.get_json()

        # Recebe a lista de equipes (pode ser uma lista de uma ou mais equipes)
        equipes = data.get("equipe")
        data_inicio = data.get("data_inicio")
        data_fim = data.get("data_fim")

        # Validação dos parâmetros
        if not equipes or not isinstance(equipes, list) or not all(isinstance(equipe, str) for equipe in equipes):
            return jsonify({"erro": "É necessário enviar uma lista de equipes, onde cada item é uma string."}), 400

        if not data_inicio or not data_fim:
            return jsonify({"erro": "É necessário enviar as datas de início e fim."}), 400

        documentos = db_handler.buscar_por_filtro(data_inicio=data_inicio, data_fim=data_fim, equipes=equipes)

        if documentos:
            # Serializa os documentos encontrados
            documentos_list = [serialize_document(doc) for doc in documentos]
            return jsonify(documentos_list), 200
        else:
            return jsonify({"message": "Nenhum documento encontrado para o filtro fornecido."}), 404

    except Exception as e:
        logger.error(f"Erro inesperado: {e}", exc_info=True)
        return jsonify({"erro": "Erro inesperado ao processar a requisição"}), 500
    
##------------ Gerar Relatorio -------------------    
@app.route('/api/gerar_relatorio', methods=['POST'])
def gerar_relatorio():
    try:
        data = request.get_json()
        
        # Valida se os dados estão presentes
        if not data or 'documentos' not in data:
            return jsonify({"error": "Payload inválido ou ausente."}), 400

        documentos = data.get('documentos', [])
        
        if not documentos:
            return jsonify({"error": "Nenhum documento foi enviado."}), 400

        data_inicio = documentos[0].get('data_inicio', '')
        data_fim = documentos[0].get('data_fim', '')
        equipes = list(set(doc.get('equipe', '') for doc in documentos if 'equipe' in doc))

        if not data_inicio or not data_fim:
            return jsonify({"error": "Data de início ou fim ausente."}), 400

        gerar_excel = GerarExcel(data_inicio, data_fim, equipes, documentos)

        arquivo_em_memoria = gerar_excel.gerar_excel_em_memoria()

        if not arquivo_em_memoria:
            return jsonify({"error": "Erro ao gerar o relatório."}), 500

        # Define o nome do arquivo para download
        filename = f"relatorio_{data_inicio}_{data_fim}.xlsx"

        # Retorna o arquivo como resposta para download
        return Response(
            arquivo_em_memoria,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment;filename={filename}'}
        )

    except Exception as e:
        print(f"Erro ao gerar o relatório: {e}")
        return jsonify({"error": f"Erro ao gerar relatório: {str(e)}"}), 500

##----------------------------------> Gerar etiquetas <------------------------------------##
@app.route('/api/gerar-etiquetas', methods=['POST'])
def gerar_etiquetas():
    """Gera etiquetas em PDF para os funcionários."""
    data = request.get_json()
    data_inicio = datetime.strptime(data.get("data_inicio"), "%Y-%m-%d").strftime("%d/%m")
    data_fim = datetime.strptime(data.get("data_fim"), "%Y-%m-%d").strftime("%d/%m/%Y")

    # Carregar funcionários
    funcionarios = CriarFuncionario.carregar_funcionarios()
    if not funcionarios:
        return jsonify({"error": "Nenhum funcionário encontrado"}), 404

    # Ordenar os funcionários por nome
    funcionarios_ordenados = sorted(funcionarios, key=lambda f: f.get("nome_funcionario", ""))

    # Configurações para o PDF
    page_width = 595  # Tamanho A4 em pontos
    page_height = 842
    etiqueta_largura = page_width / 2 - 30  # 50% da página com margens laterais
    etiqueta_altura = 72  # Altura da etiqueta ajustada para incluir 3 linhas e espaçamentos
    margem_superior = page_height - 35
    margem_lateral = 28  # Margem inicial padrão (10 mm)
    deslocamento_coluna = 22  # Deslocamento adicional para a segunda coluna
    max_linhas_por_pagina = int(page_height / etiqueta_altura)

    # Preparação do PDF
    output = BytesIO()
    c = canvas.Canvas(output, pagesize=(page_width, page_height))
    linha_atual = 0
    col_atual = 0
    y = margem_superior

    for funcionario in funcionarios_ordenados:
        nome_funcao = funcionario.get("nome_funcao", "Função Não Informada")
        if nome_funcao == "INATIVO" or nome_funcao == "-" or nome_funcao is None:
            continue

        nome_funcionario = funcionario.get("nome_funcionario", funcionario.get("numero_cpf", "Nome não disponível"))
        etiqueta_texto = f"{nome_funcionario}\n{nome_funcao}\n{data_inicio} Á {data_fim}"

        if linha_atual >= max_linhas_por_pagina:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = margem_superior
            linha_atual = 0
            col_atual = 0

        # Ajustar posição X
        x_dados = margem_lateral + (col_atual * etiqueta_largura)

        # Aplicar deslocamento apenas para a segunda coluna
        if col_atual == 1:
            x_dados += deslocamento_coluna

        c.setFont("Helvetica", 10)
        linha_y = y - 10  # Recuo inicial para alinhar à margem superior da etiqueta
        for linha in etiqueta_texto.split('\n'):
            c.drawString(x_dados, linha_y, linha)  # Texto alinhado com recuo adicional para a segunda coluna
            linha_y -= 20  # Espaçamento entre linhas

        col_atual = (col_atual + 1) % 2
        if col_atual == 0:
            y -= etiqueta_altura
            linha_atual += 1

    c.save()
    output.seek(0)
    return output.getvalue(), 200, {
        'Content-Type': 'application/pdf',
        'Content-Disposition': 'attachment; filename="etiquetas.pdf"'
    }




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

            missing_fields = [field for field in required_fields if field not in data]
            if missing_fields: 
                print(f"Campos obrigatórios faltando: {missing_fields}")
                return jsonify({"message": f"Campos obrigatórios faltando: {', '.join(missing_fields)}!"}), 400
            

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
        
        required_fields = ['nome_funcionario', 'nome_funcao', 'equipe', 'numero_cpf', 'chave_pix', 'valor_hora_base', 
                           'valor_hora_extra_um', 'valor_hora_extra_dois', 'adicional_noturno', 
                           'repouso_remunerado', 'valor_ferias', 'valor_um_terco_ferias', 
                           'valor_decimo_terceiro', 'pagamento_fgts', 'desconto_inss', 
                           'desconto_refeicao', 'desconto_transporte']
        
        if not data or any(field not in data for field in required_fields):
            return jsonify({'error': 'Dados obrigatórios faltando!'}), 400

        if colecao.find_one({'numero_cpf': data['numero_cpf']}):
            return jsonify({'error': 'Funcionário com esse CPF já existe!'}), 409

        novo_funcionario = {key: data.get(key) for key in required_fields}
        insert_result = colecao.insert_one(novo_funcionario)
        
        funcionario_id = str(insert_result.inserted_id)
        novo_funcionario['_id'] = funcionario_id
        # Consulta os dados atualizados no banco para garantir consistência
        dados_atualizados = list(colecao.find({}, {'_id': 0}))  # Exclui o campo `_id` bruto no retorno

        # Retorna uma mensagem de sucesso com o ID do novo funcionário e os dados atualizados
        return jsonify({
            'message': 'Funcionário criado com sucesso!',
            '_id': funcionario_id,
            'dados_atualizados': dados_atualizados
        }), 201

    except Exception as e:
        # Log detalhado para depuração
        print("Erro inesperado ao criar funcionário:", e)
        import traceback
        print(traceback.format_exc())
        return jsonify({'error': f'Erro interno do servidor: {str(e)}'}), 500

 
##----------------------------------> Editar cadastro do funcionário <-----------------------------------##
@app.route('/api/funcionario/<string:funcionario_id>', methods=['PUT'])
def update_funcionario(funcionario_id):
    try:
        # Converte o id do funcionário para ObjectId, caso não seja do tipo adequado
        try:
            funcionario_id = ObjectId(funcionario_id)
        except Exception as e:
            return jsonify({'message': 'ID inválido.'}), 400

        # Receber os dados do corpo da requisição
        data = request.get_json()

        # Verificar se o CPF enviado já pertence a outro funcionário
        if "numero_cpf" in data:
            cpf_novo = data["numero_cpf"]
            cpf_existente = colecao.find_one({'numero_cpf': cpf_novo})

            # Garantir que o CPF pertence ao mesmo funcionário
            if cpf_existente and str(cpf_existente['_id']) != str(funcionario_id):
                return jsonify({'message': 'Outro funcionário já possui este CPF.'}), 409

        # Atualizar os dados do funcionário no banco de dados
        resultado = colecao.update_one({'_id': funcionario_id}, {'$set': data})

        # Se não houver correspondência para o ID, retornar erro
        if resultado.matched_count == 0:
            return jsonify({'message': 'Funcionário não encontrado.'}), 404

        return jsonify({'message': 'Funcionário atualizado com sucesso.'})
        # Consultar o banco para retornar os dados atualizados do funcionário
        funcionario_atualizado = colecao.find_one({'_id': funcionario_id}, {'_id': 0})

        # Consultar todos os dados para garantir consistência no front-end
        dados_atualizados = list(colecao.find({}, {'_id': 0}))

        return jsonify({
            'message': 'Funcionário atualizado com sucesso.',
            'funcionario_atualizado': funcionario_atualizado,
            'dados_atualizados': dados_atualizados
        })

    except Exception as e:
        # Registra o erro completo no log
        app.logger.error(f"Erro ao atualizar o funcionário {funcionario_id}: {str(e)}", exc_info=True)
        return jsonify({'message': 'Erro interno ao processar a requisição.'}), 500 
    
###---------------------------------------> Criar Recibo <--------------------------------------------##

@app.route('/api/criar_recibo', methods=['POST'])
def criar_recibo():
    try:
        data = request.json
        app.logger.info(f"Dados recebidos pelo back: {data}")
    
        required_fields = [
            'data_inicio', 'data_fim', 'data_pagamento', 'name_funcionario', 'nome_cargo',
            'horas_trabalhadas', 'valor_diarias', 'horas_extras_um', 'horas_extras_dois',
            'horas_noturnas', 'correcao_positiva', 'correcao_negativa', 'parcela_vale',
            'diferenca_calculo'
        ]
        app.logger.info("Verificando campos obrigatórios...")
        if not data or any(field not in data for field in required_fields):
            app.logger.error("Dados obrigatórios faltando!")
            return jsonify({'error': 'Dados obrigatórios faltando!'}), 400
        
        # Validação e conversão de datas
        app.logger.info("Iniciando a validação e conversão das datas...")
        try:
            data['data_inicio'] = datetime.strptime(data['data_inicio'], '%d-%m-%Y').date()
            data['data_fim'] = datetime.strptime(data['data_fim'], '%d-%m-%Y').date()
            data['data_pagamento'] = datetime.strptime(data['data_pagamento'], '%d-%m-%Y').date()
            app.logger.info(f"Datas convertidas com sucesso: {data['data_inicio']}, {data['data_fim']}, {data['data_pagamento']}")
        except ValueError as e:
            app.logger.error(f"Erro na validação das datas: {e}")
            return jsonify({'error': 'Datas devem estar no formato DD-MM-YYYY!'}), 400

        # Conversão de campos numéricos
        app.logger.info("Iniciando a conversão de valores numéricos...")
        try:
            for field in [
                'horas_trabalhadas', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas',
                'valor_diarias', 'correcao_positiva', 'correcao_negativa', 'parcela_vale',
                'diferenca_calculo'
            ]:
                data[field] = float(data[field])
            app.logger.info(f"Valores numéricos convertidos com sucesso: {data}")
        except ValueError as e:
            app.logger.error(f"Erro ao converter valores numéricos: {e}")
            return jsonify({'error': 'Valores de horas devem ser numéricos!'}), 400

        
        # Busca do funcionário no banco atualizado
        app.logger.info("Carregando funcionários atualizados do banco...")
        funcionario_dict = CriarFuncionario.carregar_funcionarios()
        
        # Busca do funcionário
        funcionario_id = data['name_funcionario']
        app.logger.info(f"Buscando informações do funcionário com ID: {funcionario_id}")
        
        
        # Supondo que funcionario_dict seja uma lista de documentos de funcionários
        funcionario = next((f for f in funcionario_dict if f['_id'] == funcionario_id), None)

        if not funcionario:
            app.logger.error(f"Funcionário não encontrado: {funcionario_id}")
            return jsonify({'error': 'Funcionário não encontrado!'}), 404


        if funcionario.get('nome_funcao') == "INATIVO":
            app.logger.error(f"Funcionário {funcionario_id} está inativo!")
            return jsonify({'error': 'Funcionário está inativo!'}), 403

        # Criação do recibo
        app.logger.info("Iniciando a criação do recibo...")
        try:
            funcionario = Sub_total_um(
                data['nome_cargo'], funcionario_id, data['data_inicio'],
                data['data_fim'], data['data_pagamento']
            )
            funcionario.adicionar_horas_trabalhadas(data['horas_trabalhadas'])
            funcionario.adicionar_horas_noturnas(data['horas_noturnas'])
            funcionario.adicionar_horas_extras_um(data['horas_extras_um'])
            funcionario.adicionar_horas_extras_dois(data['horas_extras_dois'])
            funcionario.adicionar_correcao_positiva(data['correcao_positiva'])
            funcionario.adicionar_correcao_negativa(data['correcao_negativa'])
            funcionario.adicionar_valor_por_hora(data['valor_diarias'])
            funcionario.adicionar_pagamento_vale(data['parcela_vale'])
            funcionario.adicionar_diferenca_positiva(data['diferenca_calculo'])
            app.logger.info("Recibo criado com sucesso.")
        except Exception as e:
            app.logger.error(f"Erro ao criar o recibo: {e}")
            return jsonify({'error': 'Erro ao criar o recibo!'}), 500

        # Geração do PDF
        app.logger.info("Gerando o PDF do olerite...")
        try:
            olerite = Gerar_olerite(funcionario)
            buffer = olerite.gerar_sub_um()
            app.logger.info("PDF gerado com sucesso.")
        except Exception as e:
            logger.error(f"Erro ao gerar o PDF: {e}", exc_info=True)
            return jsonify({'error': 'Erro ao gerar o PDF do recibo. Consulte o administador do sistema!'}), 500

        # Envio do PDF para o cliente
        app.logger.info("Enviando o PDF gerado para o cliente...")
        return send_file(buffer, as_attachment=True, download_name='recibo.pdf', mimetype='application/pdf')

    except Exception as e:
        app.logger.error(f"Erro inesperado: {e}")
        return jsonify({'error': 'Erro ao processar a solicitação!'}), 500




##---------------------------------> Retorna Funcionarios para o Front <-------------------------------##
@app.route('/api/funcionarios/<key>', methods=['GET'])
def get_funcionario(funcionario_id):
    funcionario = funcionario_dict.get(funcionario_id)
    
    # Verifica se o funcionário existe
    if funcionario:
        # Define valores padrão para 'nome_funcionario' e 'nome_funcao' se ausentes
        funcionario.setdefault('nome_funcionario', 'Nome não cadastrado')
        funcionario.setdefault('nome_funcao', 'Função não cadastrada')
        return jsonify(funcionario), 200
    
    return jsonify({'error': 'Funcionário não encontrado'}), 404

# Função para fazer upload de arquivos para o Firebase Storage
@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Verifica se o arquivo foi enviado na requisição
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        file = request.files['file']
        
        # Verifica se o arquivo tem um nome
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        # Define o caminho local do arquivo (temporário) e o nome do arquivo no Firebase Storage
        local_file_path = os.path.join("uploads", file.filename)
        file.save(local_file_path)  # Salva o arquivo localmente no servidor
        
        storage_file_name = f"uploads/{file.filename}"  # Nome do arquivo no Firebase Storage
        
        # Faz o upload para o Firebase Storage
        upload_file_to_storage(local_file_path, storage_file_name)
        
        return jsonify({"message": f"Arquivo {file.filename} enviado para o Firebase Storage com sucesso!"}), 200
    
    except Exception as e:
        logger.error(f"Erro ao fazer upload: {e}")
        return jsonify({"error": str(e)}), 500

# Função para adicionar dados ao Firestore (exemplo de uso)
def add_to_firestore(collection_name, document_id, data):
    firestore_client = get_firestore_client()
    firestore_client.collection(collection_name).document(document_id).set(data)
    print(f"Dados adicionados à coleção {collection_name} com ID {document_id}")


# --- Outras rotas simples ---
@app.route('/')
def index():
    api_url = os.getenv('API_URL')  # Pega a URL da API do arquivo .env
    return render_template('public/index.html', api_url=api_url)

@app.route('/about')
def about():
    return "About Page"

# Listar todas as rotas (opcional, apenas para debug)
@app.route('/routes', methods=['GET'])
def list_routes():
    routes = [{"endpoint": rule.endpoint, "rule": rule.rule} for rule in app.url_map.iter_rules()]
    return jsonify(routes)

#if __name__ == "__main__":
    #port = int(os.environ.get("PORT", 5000))
    #app.run(host="0.0.0.0", port=port)

#f __name__ == "__main__":                       
 #  app.run(debug=True, port=5000)
if __name__ == '__main__':
    app.run(debug=True)