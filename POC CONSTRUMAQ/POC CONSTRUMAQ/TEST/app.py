from flask import Flask, request, jsonify, render_template, send_file, abort
from datetime import datetime
from gerar_sub_total_um import Sub_total_um
from gerador_olerite import Gerar_olerite
from criar_cargo import CriarFuncionario
import json
import os
import time
from flask import Flask
from flask_cors import CORS
import logging
from flask import Flask, send_from_directory
import uuid

# Configuração do logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

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


## --------> Criar cadastro do funcionario 



##Criação de Funcionario

@app.route('/api/funcionarios', methods=['GET', 'POST'])
def funcionarios():
    print("Requisição recebida")  # Log da requisição

    if request.method == 'POST':
        try:
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

@app.route('/api/criar_funcionario', methods=['POST'])
def criar_funcionario():
    try:
        data = request.json
        app.logger.info(f"Dados recebidos para criação de funcionário: {data}")

        required_fields = ['nome_funcionario', 'nome_funcao', 'numero_cpf', 'chave_pix', 'valor_hora_base', 
                           'valor_hora_extra_um', 'valor_hora_extra_dois', 'adicional_noturno', 
                           'repouso_remunerado', 'valor_ferias', 'valor_um_terco_ferias', 
                           'valor_decimo_terceiro', 'pagamento_fgts', 'desconto_inss', 
                           'desconto_refeicao', 'desconto_transporte']

        if not data or any(field not in data for field in required_fields):
            return jsonify({'error': 'Dados obrigatórios faltando!'}), 400

        # Gera um ID único para o novo funcionário
        funcionario_id = str(uuid.uuid4())

        # Adiciona o novo funcionário ao dicionário com o ID como chave
        funcionario_dict[funcionario_id] = {
            'nome_funcionario': data['nome_funcionario'],
            'nome_funcao': data['nome_funcao'],
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

            # Atualiza o dicionário de funcionarios
            funcionario_dict[nome] = {
                'numero_cpf': data['numero_cpf'],
                'chave_pix': data['chave_pix'],           
                'valor_hora_base': data['valor_hora_base'],
                'valor_hora_extra_um': data['valor_hora_extra_um'],
                'valor_hora_extra_dois': data['valor_hora_extra_dois'],
                'repouso_remunerado': data['repouso_remunerado'],
                'adicional_noturno': data['adicional_noturno'],
                'desconto_inss': data['desconto_inss'],
                'desconto_refeicao': data['desconto_refeicao'],
                'desconto_transporte': data['desconto_transporte'],
                'pagamento_fgts': data['pagamento_fgts'],
                'valor_decimo_terceiro': data['valor_decimo_terceiro'],
                'valor_ferias': data['valor_ferias'],
                'valor_um_terco_ferias': data['valor_um_terco_ferias']
            }
            
            # Salva os cargos no arquivo
            CriarFuncionario.salvar_cargos(funcionario_dict)
            return jsonify({"message": "Cargo cadastrado com sucesso!"}), 201
        
        except Exception as e:
            print(f"Erro ao cadastrar cargo: {e}")
            return jsonify({"message": "Erro ao cadastrar cargo!"}), 500


    elif request.method == 'GET':
        return jsonify(funcionario_dict)

        app.logger.info(f'Funcionário {data["nome_funcionario"]} criado com sucesso com ID: {funcionario_id}.')
        return jsonify({'message': 'Funcionário criado com sucesso!', 'data': funcionario_dict[funcionario_id]}), 201

    except Exception as e:
        app.logger.error(f'Erro ao criar funcionário: {str(e)}')
        return jsonify({'error': 'Erro interno do servidor.'}), 500


    


## --------> Editar o cadastro do Funcionario 

@app.route('/api/funcionario/<string:funcionario_id>', methods=['PUT'])
def editar_funcionario(funcionario_id):
    logger.debug(f'Tentando atualizar o funcionário com id: {funcionario_id}')

    # Verifica se o ID é nome (antigo) ou uid (novo)
    if funcionario_id not in funcionario_dict:
        logger.warning(f'Funcionário com id {funcionario_id} não encontrado')
        return jsonify({'message': 'Funcionário não encontrado'}), 404

    data = request.json


    # Atualiza os dados do funcionário

    funcionarios_db[nomeFuncionario]['numero_cpf'] = data.get('cpf', funcionarios_db[nomeFuncionario]['numero_cpf'])
    funcionarios_db[nomeFuncionario]['chave_pix'] = data.get('chave_pix', funcionarios_db[nomeFuncionario]['chave_pix'])
    funcionarios_db[nomeFuncionario]['valor_hora_base'] = data.get('valor_hora_base', funcionarios_db[nomeFuncionario]['valor_hora_base'])
    funcionarios_db[nomeFuncionario]['valor_hora_extra_um'] = data.get('valor_hora_extra_um', funcionarios_db[nomeFuncionario]['valor_hora_extra_um'])
    funcionarios_db[nomeFuncionario]['valor_hora_extra_dois'] = data.get('valor_hora_extra_dois', funcionarios_db[nomeFuncionario]['valor_hora_extra_dois'])
    funcionarios_db[nomeFuncionario]['adicional_noturno'] = data.get('adicional_noturno', funcionarios_db[nomeFuncionario]['adicional_noturno'])
    funcionarios_db[nomeFuncionario]['repouso_remunerado'] = data.get('repouso_remunerado', funcionarios_db[nomeFuncionario]['repouso_remunerado'])
    funcionarios_db[nomeFuncionario]['valor_ferias'] = data.get('valor_ferias', funcionarios_db[nomeFuncionario]['valor_ferias'])
    funcionarios_db[nomeFuncionario]['valor_um_terco_ferias'] = data.get('valor_um_terco_ferias', funcionarios_db[nomeFuncionario]['valor_um_terco_ferias'])
    funcionarios_db[nomeFuncionario]['valor_decimo_terceiro'] = data.get('valor_decimo_terceiro', funcionarios_db[nomeFuncionario]['valor_decimo_terceiro'])
    funcionarios_db[nomeFuncionario]['pagamento_fgts'] = data.get('pagamento_fgts', funcionarios_db[nomeFuncionario]['pagamento_fgts'])
    funcionarios_db[nomeFuncionario]['desconto_inss'] = data.get('desconto_inss', funcionarios_db[nomeFuncionario]['desconto_inss'])
    funcionarios_db[nomeFuncionario]['desconto_refeicao'] = data.get('desconto_refeicao', funcionarios_db[nomeFuncionario]['desconto_refeicao'])
    funcionarios_db[nomeFuncionario]['desconto_transporte'] = data.get('desconto_transporte', funcionarios_db[nomeFuncionario]['desconto_transporte'])
     
    logger.info(f'Funcionário {nomeFuncionario} atualizado com sucesso: {funcionarios_db[nomeFuncionario]}')
    return jsonify({'message': 'Funcionário atualizado com sucesso', 'data': funcionarios_db[nomeFuncionario]}), 200



    # Checa se é um registro antigo sem UID
    if not isinstance(funcionario_id, str) or len(funcionario_id) != 36:
        # Criar um novo UID para o registro
        novo_uid = str(uuid.uuid4())
        funcionario_dict[novo_uid] = funcionario_dict.pop(funcionario_id)
        funcionario_dict[novo_uid]["nome_funcionario"] = funcionario_id  # Mantém o nome como `nome_funcionario`
        funcionario_id = novo_uid  # Atualiza para a nova chave UID
    
    funcionario = funcionario_dict[funcionario_id]
    
    # Verifica e adiciona campo `nome_funcao` se estiver ausente
    funcionario.setdefault('nome_funcao', data.get('nome_funcao', ''))

    # Atualiza os dados com os valores recebidos
    campos = ['nome_funcionario', 'nome_funcao', 'numero_cpf', 'chave_pix', 'valor_hora_base',
              'valor_hora_extra_um', 'valor_hora_extra_dois', 'adicional_noturno', 'repouso_remunerado',
              'valor_ferias', 'valor_um_terco_ferias', 'valor_decimo_terceiro', 'pagamento_fgts', 
              'desconto_inss', 'desconto_refeicao', 'desconto_transporte']
    
    for campo in campos:
        if campo in data:
            funcionario[campo] = data[campo]
    
    CriarFuncionario.salvar_cargos(funcionario_dict)
    logger.info(f'Funcionário {funcionario_id} atualizado com sucesso: {funcionario}')
    return jsonify({'message': 'Funcionário atualizado com sucesso', 'data': funcionario}), 200

   
## --------> Cria o funcionario e gera o recibo

@app.route('/api/criar_recibo', methods=['POST'])
def criar_recibo():
        
        data = request.json 
        
        #1 logg
        app.logger.info(f"Dados recebidos pelo back: {data}")


        required_fields = [ 'data_inicio','data_fim', 'data_pagamento','name_funcionario','nome_cargo', 'horas_trabalhadas','valor_diarias', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas', 'correcao_positiva', 'correcao_negativa']
 
        
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

            for field in ['horas_trabalhadas', 'horas_extras_um', 'horas_extras_dois', 'horas_noturnas', 'valor_diarias', 'correcao_positiva', 'correcao_negativa']:

                data[field] = float(data[field])
        except ValueError as e:
            app.logger.error(f"Erro ao converter valores: {e}")
            return jsonify({'error': 'Valores de horas devem ser numéricos!'}), 400

        funcionario_id= data['name_funcionario']
        funcionario = funcionario_dict.get(funcionario_id)

        if not funcionario:
            return jsonify({'error': 'Funcionario não encontrado!'}), 404   

        # Cria o objeto funcionario com base nos dados recebidos
        
        data = request.get_json()  # Ou request.form se for um form HTML
        print(f"Dados da requisição: {data}")

        funcionario = Sub_total_um(data['nome_cargo'], funcionario_id , data['data_inicio'], data['data_fim'], data['data_pagamento'])

        # Adicionando as horas e outros dados   
        
        funcionario.adicionar_horas_trabalhadas(data['horas_trabalhadas'])
        funcionario.adicionar_horas_noturnas(data['horas_noturnas'])
        funcionario.adicionar_horas_extras_um(data['horas_extras_um'])
        funcionario.adicionar_horas_extras_dois(data['horas_extras_dois'])
        funcionario.adicionar_correcao_positiva(data['correcao_positiva']) 
        funcionario.adicionar_correcao_negativa(data['correcao_negativa']) 
        funcionario.adicionar_valor_por_hora(data['valor_diarias'])
        
        # Gerar o olerite
        olerite = Gerar_olerite(funcionario)
        buffer = olerite.gerar_sub_um()
        
        return send_file(buffer, as_attachment=True, download_name='recibo.pdf', mimetype='application/pdf')



# --------> Retorna o nome do funcionário e o cargo
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


                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
@app.route('/baixar_excel', methods=['GET'])
def baixar_excel():
    # Caminho completo do arquivo
    diretorio = os.path.join(app.root_path, 'static')
    caminho_arquivo = os.path.join(diretorio, 'dados_de_pagamento.xlsx')
    
    # Verifica se o arquivo existe
    if not os.path.exists(caminho_arquivo):
        abort(404, "Arquivo não encontrado")

    # Envia o arquivo para download, especificando o tipo de conteúdo
    return send_file(caminho_arquivo, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')




#Editar Funcionario 

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
    app.run(debug=True, port=5000)
    
      
