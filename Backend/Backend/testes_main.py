from gerar_sub_total_um import Sub_total_um
from gerador_olerite import Gerar_olerite

def criar_funcionario():
    nome_cargo = input("Digite o cargo do funcionário: ")
    nome_funcionario = input("Digite o nome do funcionário: ")
    horas_trabalhadas = float(input("Digite as horas trabalhadas: "),2)
    repouso_remunerado = float(input("Digite horas respouso remunerado : "),2)
    horas_extras_um = float(input("Digite a quantidade de horas extras de 50%: "),2)
    horas_extras_dois = float(input("Digite a quantidade de horas extras de 100%: "),2)
    horas_noturnas = float(input("Digite a quantidade de horas noturnas: "),2)
    adiantamento_salario = float(input("Digite adiantamento salarial: "),2)
    
    
    

    funcionario = Sub_total_um(nome_funcionario, nome_cargo)
    funcionario.adicionar_horas_trabalhadas(horas_trabalhadas)
    funcionario.adicionar_horas_repouso(repouso_remunerado)
    funcionario.adicionar_horas_noturnas(horas_noturnas)
    funcionario.adicionar_horas_extras_um(horas_extras_um)
    funcionario.adicionar_horas_extras_dois(horas_extras_dois)
    funcionario.adicionar_adiantamento_salarial(adiantamento_salario)
    
    
    return funcionario


    

def main():
    print("\nCriando Funcionário:")
    funcionario = criar_funcionario()

    print("\nObjeto do Funcionário Criado:")
    print(funcionario)

    print("\nGeração do Olerite:")
    gerar_documento = Gerar_olerite(funcionario)
    print(gerar_documento.gerar_sub_um())

if __name__ == "__main__":
    main()
