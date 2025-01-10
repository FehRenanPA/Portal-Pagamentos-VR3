from pymongo import MongoClient
from bson import ObjectId
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Conectar ao MongoDB
uri = os.getenv('MONGO_URI')  # Certifique-se de que o MONGO_URI está configurado corretamente no .env
client = MongoClient(uri)

# Selecionar o banco de dados e a coleção
db = client['FUNCIONARIOS_VR3_PAGAMENTOS']  # Substitua pelo nome do seu banco de dados real
colecao = db['funcionario']  # Nome da coleção

# Ler os dados do arquivo JSON
with open('funcionario.json', 'r', encoding='utf-8') as file:
    dados_funcionarios = json.load(file)  # Carregar os dados do arquivo JSON

# Processar e migrar os dados
for uid, dados in dados_funcionarios.items():
    # Remover o UID como chave e adicionar um _id padrão do MongoDB
    dados['_id'] = ObjectId()  # Gerar um novo ObjectId

    # Inserir ou atualizar os dados no MongoDB
    colecao.update_one(
        {'_id': dados['_id']},  # Condição para identificar o registro
        {'$set': dados},  # Dados a serem atualizados/inseridos
        upsert=True  # Inserir se não existir
    )

# Imprimir os dados migrados
print("Funcionários transformados e inseridos/atualizados no banco de dados:")
for funcionario in colecao.find():
    print(funcionario)
