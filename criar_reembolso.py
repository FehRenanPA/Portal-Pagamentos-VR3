import json
import os
from pymongo import MongoClient
from cargo_reembolso import FuncionarioReembolso
from dotenv import load_dotenv


MONGO_URI = os.getenv('MONGO_URI')
client = MongoClient(MONGO_URI)
db = client['FUNCIONARIOS_VR3_PAGAMENTOS']
colecao_reembolso = db['reembolso']

load_dotenv()


class CriarReembolso:
    funcionario_dict_reembolso = {}

    @staticmethod
    def carregar_funcionario_reembolso():
        """
        Carrega todos os funcionários na seguinte ordem:
        1. MongoDB.
        2. Cache na memória (funcionario_dict).
        3. Arquivo JSON.
        """
        # 1. Tenta carregar do MongoDB
        try:
            funcionarios_reembolso = colecao_reembolso.find()  # Recupera todos os documentos
            funcionario_dict_reembolso = {str(func['_id']): func for func in funcionarios_reembolso}
            CriarReembolso.funcionario_dict_reembolso = funcionario_dict_reembolso  # Atualiza o cache
            print("Funcionários para reembolso carregados do MongoDB e cache atualizado.")
            return funcionario_dict_reembolso
        except Exception as e:
            print(f"Erro ao carregar do MongoDB: {e}")

        # 2. Tenta carregar do cache
        if CriarReembolso.funcionario_dict_reembolso:
            print("Funcionários carregados do cache.")
            return CriarFuncionarioReembolso.funcionario_dict

        # 3. Tenta carregar do arquivo JSON
        try:
            if os.path.exists('funcionario.json'):
                with open('funcionario.json', 'r') as file:
                    funcionarios_reembolso = json.load(file)
                    CriarFuncionarioReembolso.funcionario_dict = funcionarios_reembolso  # Atualiza o cache
                    print("Funcionários carregados do arquivo JSON e cache atualizado.")
                    return funcionarios_reembolso
        except Exception as e:
             print(f"Erro ao carregar do arquivo JSON: {e}")

        # 4. Se nenhuma fonte for encontrada, retorna vazio
        print("Nenhuma fonte disponível para carregar os funcionários.")
        return {}    

    @staticmethod
    def carregar_reembolso_por_id(reembolso_id):
        """Carrega um reembolso específico pelo ID."""
        try:
            # Recupera o reembolso do MongoDB com o ID fornecido
            reembolso = colecao_reembolso.find_one({"_id": reembolso_id})
            if reembolso:
                reembolso['_id'] = str(reembolso['_id'])  # Converte o _id para string
            return reembolso
        except Exception as e:
            print(f"Erro ao carregar reembolso por ID: {e}")
            return None

    @staticmethod
    def criar_funcionario_reembolso(data):
        """Cria um novo funcionário e salva no MongoDB."""
        name = data['name']
        nome_funcao = data['nome_funcao']
        equipe = data['equipe']
        numero_cpf = data['numero_cpf']
        chave_pix = data['chave_pix']
        valor_hora_base = round(float(data['valor_hora_base']), 2)
        valor_hora_extra_um = round(float(data['valor_hora_extra_um']), 2)
        valor_hora_extra_dois = round(float(data['valor_hora_extra_dois']), 2)
        adicional_noturno = round(float(data['adicional_noturno']), 2)
        repouso_remunerado = round(float(data['repouso_remunerado']), 2)
        valor_ferias = round(float(data['valor_ferias']) / 100, 2)
        valor_antecipa_ferias = round(float(data['valor_antecipa_ferias']) / 100, 2)
        valor_decimo_terceiro = round(float(data['valor_decimo_terceiro']) / 100, 2)
        valor_antecipa_salario = round(float(data['valor_antecipa_salario']), 2)
        pagamento_fgts = round(float(data['pagamento_fgts']) / 100, 2)
        desconto_inss = round(float(data['desconto_inss']) / 100, 2)
        desconto_refeicao = round(float(data['desconto_refeicao']), 2)
        desconto_transporte = round(float(data['desconto_transporte']), 2)
        cnpj_empresa = data['cnpj_empresa']
        empresa = data['empresa']
        salario_base = round(float(data['salario_base']), 2)

        # Cria a instância de Funcionario
        funcionario_reembolso = Funcionario(name, nome_funcao, equipe, numero_cpf, chave_pix, valor_hora_base, adicional_noturno,
                                  valor_hora_extra_um, valor_hora_extra_dois, repouso_remunerado, valor_ferias,
                                  valor_antecipa_ferias, valor_decimo_terceiro, valor_antecipa_salario, pagamento_fgts,
                                  desconto_inss, desconto_refeicao, desconto_transporte, empresa, cnpj_empresa, salario_base)
        
        # Salva no MongoDB
        colecao_reembolso.insert_one(reembolso.to_dict())  # Salva o funcionário no MongoDB
        print(f"Funcionário {name} criado com sucesso.")

    @staticmethod
    def salvar_funcionarios():
        """Salva os funcionários no arquivo JSON (caso seja necessário)."""
        with open('funcionario.json', 'w') as file:
            json.dump(CriarReembolso.funcionario_dict, file)
            print("Funcionários salvos no arquivo JSON.")

    @staticmethod
    def editar_funcionario(nome_funcionario, novos_dados):
        """Edita um funcionário no banco de dados MongoDB."""
        funcionario = colecao_reembolso.find_one({"name": nome_funcionario})
        if funcionario:
            # Atualiza os dados do funcionário
            colecao_reembolso.update_one({"name": nome_funcionario}, {"$set": novos_dados})
            print(f"Funcionário {nome_funcionario} atualizado com sucesso!")
        else:
            print(f"Funcionário {nome_funcionario} não encontrado.")

    @staticmethod
    def excluir_funcionario(nome_funcionario):
        """Exclui um funcionário do MongoDB."""
        colecao_reembolso.delete_one({"name": nome_funcionario})
        print(f"Funcionário {nome_funcionario} excluído com sucesso.")


def main():
    CriarReembolso.funcionario_dict = CriarReembolso.carregar_funcionario_reembolso()
    print(f"Cargos carregados: {CriarReembolso.funcionario_dict}")

    while True:
        print("\nMenu:")
        print("1. Criar Cargo")
        print("2. Editar Cargo")
        print("3. Excluir Cargo")
        print("4. Sair")
        
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            data = {
                'name': input("Nome do cargo: "),
                'valor_hora_base': input("Valor da hora base: "),
                'valor_hora_extra_um': input("Valor da hora extra 50%: "),
                'valor_hora_extra_dois': input("Valor da hora extra 100%: "),
                'adicional_noturno': input("Adicional noturno: "),
                'repouso_remunerado': input("Repouso remunerado: "),
                'valor_ferias': input("Valor de férias: "),
                'valor_antecipa_ferias': input("Valor de antecipação de férias: "),
                'valor_decimo_terceiro': input("Valor do décimo terceiro: "),
                'valor_antecipa_salario': input("Valor de antecipação salarial: "),
                'pagamento_fgts': input("Pagamento de FGTS: "),
                'desconto_inss': input("Desconto de INSS: "),
                'desconto_refeicao': input("Desconto de refeição: "),
                'desconto_transporte': input("Desconto de transporte: ")
            }
            CriarFuncionario.criar_funcionario(data)
        elif escolha == '2':
            nome_funcionario = input("Digite o nome do funcionário a ser editado: ")
            novos_dados = {
                "nome_funcao": input(f"Nova função: "),
                "equipe": input(f"Nova equipe: "),
                "numero_cpf": input(f"Novo CPF: "),
                # Adicionar mais campos aqui conforme necessário
            }
            CriarFuncionario.editar_funcionario(nome_funcionario, novos_dados)
        elif escolha == '3':
            nome_funcionario = input("Digite o nome do funcionário a ser excluído: ")
            CriarFuncionario.excluir_funcionario(nome_funcionario)
        elif escolha == '4':
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
