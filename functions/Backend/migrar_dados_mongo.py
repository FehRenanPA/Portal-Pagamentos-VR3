from pymongo import MongoClient
import json
import os
import uuid
from dotenv import load_dotenv

# URI de conexão com MongoDB Atlas
load_dotenv()
#uri = os.getenv("MONGO_URI")  # Usando variável de ambiente para maior segurança
uri=os.getenv("MONGO_URI")
# Conectar ao MongoDB
client = MongoClient(uri)

# Selecionar o banco de dados
db = client['FUNCIONARIOS_VR3_PAGAMENTOS']  # Substitua pelo nome do seu banco de dados real

# Selecionar a coleção (tabela) onde os dados serão armazenados
colecao = db['funcionario']  # Nome da coleção

# Abrir o arquivo JSON
with open('funcionario.json', 'r', encoding='utf-8') as file:
    dados_funcionarios = json.load(file)  # Carregar os dados do arquivo JSON

# Migrar os dados para o MongoDB
for chave, dados in dados_funcionarios.items():
    dados['_id'] = str(uuid.uuid4())  # Gerar um UUID único como ID
    colecao.update_one(
        {'_id': dados['_id']},  # Condição para verificar se o registro já existe
        {'$set': dados},  # Atualizar os dados
        upsert=True  # Insere o documento se ele ainda não existir
    )

# Verificar se os dados foram inseridos/atualizados
print("Funcionários inseridos/atualizados no banco de dados:")
for funcionario in colecao.find():
    print(funcionario)
