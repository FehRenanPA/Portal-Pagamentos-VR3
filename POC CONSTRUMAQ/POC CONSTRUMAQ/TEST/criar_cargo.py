import json
import os
from cargo import Funcionario


class CriarFuncionario:
    funcionario_dict = {}

    @staticmethod
    def carregar_funcionarios():
         if os.path.exists('funcionario.json'):
            with open('funcionario.json', 'r') as file:
                funcionarios = json.load(file)
                print(f"Funcionários carregados: {funcionarios}")
                return funcionarios
         return {}

    @staticmethod
    def criar_funcionario(data):
        name = data['name']
        nome_funcao = data['nome_funcao']
        equipe=data['equipe']
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

        funcionario = Funcionario(name,nome_funcao,equipe, numero_cpf,chave_pix,valor_hora_base, adicional_noturno, valor_hora_extra_um,
                      valor_hora_extra_dois, repouso_remunerado, valor_ferias,
                      valor_antecipa_ferias, valor_decimo_terceiro, valor_antecipa_salario,
                      pagamento_fgts, desconto_inss, desconto_refeicao, desconto_transporte)
        
        CriarFuncionario.funcionario_dict[name] = funcionario.to_dict()
        CriarFuncionario.salvar_funcionarios()
        print(f"Cargo {name} criado com sucesso e adicionado ao dicionário.")  
    
    def to_dict(self):
        return {
            'name': self.name,
            'nome_funcao': self.nome_funcao,
            'equipe': self.equipe,
            'numero_cpf': self.numero_cpf,
            'chave_pix': self.chave_pix,
            'valor_hora_base': self.valor_hora_base,
            'valor_hora_extra_um': self.valor_hora_extra_um,
            'valor_hora_extra_dois': self.valor_hora_extra_dois,
            'adicional_noturno': self.adicional_noturno,
            'repouso_remunerado': self.repouso_remunerado,
            'valor_ferias': self.valor_ferias,
            'valor_antecipa_ferias': self.valor_antecipa_ferias,
            'valor_decimo_terceiro': self.valor_decimo_terceiro,
            'valor_antecipa_salario': self.valor_antecipa_salario,
            'pagamento_fgts': self.pagamento_fgts,
            'desconto_inss': self.desconto_inss,
            'desconto_refeicao': self.desconto_refeicao,
            'desconto_transporte': self.desconto_transporte
        }        

   
    @staticmethod
    def salvar_funcionarios():
        with open('funcionario.json', 'w') as file:
            json.dump(CriarFuncionario.funcionario_dict, file)

def editar_funcionario():
    # Carregar os dados dos funcionários
    funcionarios = CriarFuncionario.carregar_funcionario()
    
    if not funcionarios:
        print("Nenhum funcionário disponível para editar.")
        return
    
    # Exibir lista de funcionários disponíveis
    print(f"Funcionários disponíveis: {list(funcionarios.keys())}")
    
    # Solicitar o nome do funcionário a ser editado
    nome_funcionario = input("Digite o nome do funcionário que deseja editar: ")
    
    if nome_funcionario not in funcionarios:
        print(f"Funcionário {nome_funcionario} não encontrado.")
        return
    
    # Exibir os dados atuais do funcionário
    print(f"Dados atuais do funcionário {nome_funcionario}: {funcionarios[nome_funcionario]}")
    
    # Atualizar os valores do funcionário
    funcionario_atual = funcionarios[nome_funcionario]
    nome_funcao = input(f"Digite a nova funnçao (atual: {funcionario_atual['nome_funcao']}): ") or funcionario_atual['nome_funcao']
    equipe = input(f"Digite a nova funnçao (atual: {funcionario_atual['equipe']}): ") or funcionario_atual['equipe']
    numero_cpf = input(f"Digite o novo CPF (atual: {funcionario_atual['numero_cpf']}): ") or funcionario_atual['numero_cpf']
    chave_pix = input(f"Digite a nova chave PIX (atual: {funcionario_atual['chave_pix']}): ") or funcionario_atual['chave_pix']
    valor_hora_base = float(input(f"Digite o novo valor da hora base (atual: {funcionario_atual['valor_hora_base']}): ") or funcionario_atual['valor_hora_base'])
    valor_hora_extra_um = float(input(f"Digite o novo valor da hora extra 50% (atual: {funcionario_atual['valor_hora_extra_um']}): ") or funcionario_atual['valor_hora_extra_um'])
    valor_hora_extra_dois = float(input(f"Digite o novo valor da hora extra 100% (atual: {funcionario_atual['valor_hora_extra_dois']}): ") or funcionario_atual['valor_hora_extra_dois'])
    adicional_noturno = float(input(f"Digite o novo adicional noturno (atual: {funcionario_atual['adicional_noturno']}): ") or funcionario_atual['adicional_noturno'])
    repouso_remunerado = float(input(f"Digite o novo valor do repouso remunerado (atual: {funcionario_atual['repouso_remunerado']}): ") or funcionario_atual['repouso_remunerado'])
    desconto_inss = float(input(f"Digite o novo desconto INSS (atual: {funcionario_atual['desconto_inss']}): ") or funcionario_atual['desconto_inss'])
    desconto_refeicao = float(input(f"Digite o novo desconto de refeição (atual: {funcionario_atual['desconto_refeicao']}): ") or funcionario_atual['desconto_refeicao'])
    desconto_transporte = float(input(f"Digite o novo desconto de transporte (atual: {funcionario_atual['desconto_transporte']}): ") or funcionario_atual['desconto_transporte'])
    pagamento_fgts = float(input(f"Digite o novo valor do FGTS (atual: {funcionario_atual['pagamento_fgts']}): ") or funcionario_atual['pagamento_fgts'])
    valor_decimo_terceiro = float(input(f"Digite o novo valor do 13º salário (atual: {funcionario_atual['valor_decimo_terceiro']}): ") or funcionario_atual['valor_decimo_terceiro'])
    valor_ferias = float(input(f"Digite o novo valor das férias (atual: {funcionario_atual['valor_ferias']}): ") or funcionario_atual['valor_ferias'])
    valor_um_terco_ferias = float(input(f"Digite o novo valor de 1/3 das férias (atual: {funcionario_atual['valor_um_terco_ferias']}): ") or funcionario_atual['valor_um_terco_ferias'])
    
    # Atualizar os dados do funcionário
    funcionarios[nome_funcionario] = {
        'nome_funcao':nome_funcao,
        'equioe':equipe,
        'numero_cpf': numero_cpf,
        'chave_pix': chave_pix,
        'valor_hora_base': valor_hora_base,
        'valor_hora_extra_um': valor_hora_extra_um,
        'valor_hora_extra_dois': valor_hora_extra_dois,
        'adicional_noturno': adicional_noturno,
        'repouso_remunerado': repouso_remunerado,
        'desconto_inss': desconto_inss,
        'desconto_refeicao': desconto_refeicao,
        'desconto_transporte': desconto_transporte,
        'pagamento_fgts': pagamento_fgts,
        'valor_decimo_terceiro': valor_decimo_terceiro,
        'valor_ferias': valor_ferias,
        'valor_um_terco_ferias': valor_um_terco_ferias
    }
    
    # Salvar as alterações
    CriarFuncionario.salvar_funcionarios(funcionarios)
    print(f"Funcionário {nome_funcionario} atualizado com sucesso.")


def main():
    CriarFuncionario.funcionario_dict = CriarFuncionario.carregar_funcionario()
    print(f"Cargos carregados: {CriarFuncionario.funcionario_dict}")
    
    while True:
        print("\nMenu:")
        print("1. Criar Cargo")
        print("2. Editar Cargo")
        print("3. Sair")
        
        escolha = input("Escolha uma opção: ")
        if escolha == '1':
            data = {}
            data['name'] = input("Nome do cargo: ")
            data['valor_hora_base'] = input("Valor da hora base: ")
            data['valor_hora_extra_um'] = input("Valor da hora extra 50%: ")
            data['valor_hora_extra_dois'] = input("Valor da hora extra 100%: ")
            data['adicional_noturno'] = input("Adicional noturno: ")
            data['repouso_remunerado'] = input("Repouso remunerado: ")
            data['valor_ferias'] = input("Valor de férias: ")
            data['valor_antecipa_ferias'] = input("Valor de antecipação de férias: ")
            data['valor_decimo_terceiro'] = input("Valor do décimo terceiro: ")
            data['valor_antecipa_salario'] = input("Valor de antecipação salarial: ")
            data['pagamento_fgts'] = input("Pagamento de FGTS: ")
            data['desconto_inss'] = input("Desconto de INSS: ")
            data['desconto_refeicao'] = input("Desconto de refeição: ")
            data['desconto_transporte'] = input("Desconto de transporte: ")
            
            CriarFuncionario.criar_funcionario(data)
        elif escolha == '2':
            editar_funcionario()
        elif escolha == '3':
            break
        else:
            print("Opção inválida. Tente novamente.")





if __name__ == "__main__":
    main()