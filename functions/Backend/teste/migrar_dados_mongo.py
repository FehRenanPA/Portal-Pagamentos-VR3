from pymongo import MongoClient
import json

# URI de conexão com MongoDB Atlas
uri = "mongodb+srv://vr3_Engernharia:Construmaq1010@cluster0.3fjax.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

# Selecionar o banco de dados
db = client['meu_banco']  # 'meu_banco' pode ser o nome do banco de dados que você deseja usar

# Selecionar a coleção (tabela) onde os dados serão armazenados
colecao = db['funcionarios']  # 'funcionarios' é o nome da coleção

# Abrir o arquivo JSON
with open('funcionario.json', 'r', encoding='utf-8') as file:
    dados_funcionarios = json.load(file)  # Carregar os dados do arquivo JSON

# Migrar os dados para o MongoDB
for chave, dados in dados_funcionarios.items():
    dados['_id'] = chave  # Usar o UUID como o ID único do MongoDB
    colecao.insert_one(dados)  # Inserir o documento na coleção

# Verificar se os dados foram inseridos
print("Funcionários inseridos no banco de dados:")
for funcionario in colecao.find():
    print(funcionario)
