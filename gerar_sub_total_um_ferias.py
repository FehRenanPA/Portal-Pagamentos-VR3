from datetime import datetime
import holidays
import pandas as pd
from criar_cargo import CriarFuncionario
import logging

#funcionario_dict = CriarFuncionario.carregar_funcionarios()

# Valida se os dados foram carregados corretamente
class Sub_total_um_ferias:

    def __init__(self, nome_cargo, name_funcionario,data_inicio,data_fim,data_pagamento,empresa_exe):
        self.nome_cargo= nome_cargo
        self.name_funcionario = name_funcionario
        self.data_inicio= data_inicio
        self.data_fim= data_fim
        self.data_pagamento = data_pagamento
        self.horas_trabalhadas = 0
        self.empresa_exe = empresa_exe
        self.horas_extras_um = 0
        self.horas_extras_dois = 0
        self.horas_noturnas = 0
        self.repouso_remunerado = 0
        self.valor_ferias = 0
        self.correcao_positiva = 0
        self.correcao_negativa = 0
        self.parcela_vale=0
        self.valor_diarias = 0
        self.mais = 0
        self.menos = 0
        self.diferenca_calculo = 0
        self.faltas = 0
        
      

        
        

    
    def adicionar_horas_trabalhadas(self, horas):
        self.horas_trabalhadas += horas
        

    #def adicionar_horas_repouso(self, horas):
        #self.repouso_remunerado += horas    
    def adicionar_horas_repouso(self, horas):
        self.repouso_remunerado += horas    

        
    def adicionar_horas_extras_um(self, horas):
        self.horas_extras_um += horas   # 50%
    
    def adicionar_horas_extras_dois(self, horas):
        self.horas_extras_dois += horas    #100%

    def adicionar_horas_noturnas(self, horas):
        self.horas_noturnas += horas 
        
    def adicionar_pagamento_ferias(self,valor):
        self.valor_ferias += valor       

    def adicionar_pagamento_vale(self,valor):    
            self.parcela_vale += valor    

    def adicionar_correcao_positiva(self, valor):
        self.correcao_positiva += valor

    def adicionar_correcao_negativa(self, valor):
        self.correcao_negativa += valor
        
        
    def adicionar_valor_por_hora(self,valor):    
        self.valor_diarias += valor


    def adicionar_diferenca_positiva(self,valor):    
        self.diferenca_calculo += valor 

    def valor_faltas(self,valor):    
        self.faltas += valor 

    def contar_dias_mes_para(self):
        if self.data_pagamento:
            ref_date = pd.to_datetime(self.data_pagamento)
        else:
            ref_date = pd.Timestamp.today()

        inicio = ref_date.replace(day=1)
        fim = ref_date + pd.offsets.MonthEnd(0)
        
        todas_as_datas = pd.date_range(start=inicio, end=fim)
        total_dias = len(todas_as_datas)

        print(f"Mês de referência: {inicio.strftime('%m/%Y')} | Total de dias do mês: {total_dias}")

        return {"dias_uteis": total_dias}
        
    def valida_funcionario(self):
        #Bucar somente quando a class  gerar olerite for chamada
        funcionario_dict = CriarFuncionario.carregar_funcionarios()
        print(f"Cargos disponíveis: {list(funcionario_dict.keys())}")
        
        funcionario_normalizado = self.name_funcionario.strip().lower()
        # Normaliza o dicionário de cargos para comparação
        funcionario_dict_normalizado = {k.strip().lower(): v for k, v in funcionario_dict.items()}
        
        if funcionario_normalizado in funcionario_dict_normalizado:
            self.funcionario = funcionario_dict_normalizado[funcionario_normalizado]  # Armazena o objeto Funcionario
            return True
        else:
            print("Funcionario não encontrado!")
            logging.error(f"Funcionário {self.name_funcionario} não encontrado!")
            return False  # Retorna False se não encontrar o funcionário

    
    def calcular_pagamento_um(self)-> dict:
        if not self.valida_funcionario():
            logging.error("Validação do funcionário falhou.")
            return {
            'sub_total_tres': 0.00,
            'sub_total_um': 0.00,
            'sub_total_dois': 0.00
        }
        
        valor_hora_base = self.funcionario['valor_hora_base']
        valor_repouso_remunerado = self.funcionario['repouso_remunerado']
        valor_hora_extra_um = self.funcionario['valor_hora_extra_um']
        valor_hora_extra_dois = self.funcionario['valor_hora_extra_dois']
        adicional_noturno = self.funcionario['adicional_noturno']
        desconto_refeicao =self.funcionario['desconto_refeicao']
        desconto_transporte = self.funcionario['desconto_transporte']
        
       
        
            
        #ADICIONAIS
        faltas = self.faltas
        salario_base_mes = valor_hora_base * (220)
        d_s_r = self.repouso_remunerado /(7.33)
        faltas_d_s_r = salario_base_mes / (30) * self.faltas
       
        #SUB-TATAL 1
        pagamento_base = self.horas_trabalhadas * valor_hora_base
        pagamento_horas_extras_um = self.horas_extras_um * valor_hora_extra_um
        pagamento_horas_extras_dois = self.horas_extras_dois * valor_hora_extra_dois
        pagamento_adicional_noturno = self.horas_noturnas * adicional_noturno
        
        if self.horas_trabalhadas < 44 :
           self.repouso_remunerado = 0
            

        pagamento_folga_remunerada = self.repouso_remunerado * valor_repouso_remunerado  

         # Puxa dinamicamente os dias úteis e de folga calculados pelo estado do Pará
        dias_calculados = self.contar_dias_mes_para()
        dias_uteis = dias_calculados["dias_uteis"]

        # Evita divisão por zero caso o período venha zerado por algum motivo                                                                                                                                                                                                 
        dias_trabalhos = self.horas_trabalhadas / (7.33) 
        d_s_r_adicionais = ((pagamento_horas_extras_um +
                        pagamento_horas_extras_dois +
                        pagamento_adicional_noturno) / dias_trabalhos ) * d_s_r
        
        print(f"Horas Trabalhadas: {self.horas_trabalhadas } e Hora ({valor_hora_base}) ")

        print(f"Dias Úteis: {dias_uteis} ")
        print(f"Dias trabalhos: {dias_trabalhos}")
        print(f"DSR: {d_s_r_adicionais}")
        
        sub_total_um = (pagamento_base + 
                        pagamento_horas_extras_um +
                        pagamento_horas_extras_dois +
                        pagamento_adicional_noturno + 
                        pagamento_folga_remunerada + d_s_r_adicionais) 

                        

        
        #SUB-TOTAL 2
        
        sub_total_dois = (pagamento_base + pagamento_folga_remunerada) * desconto_refeicao/100
        sub_total_tres = (pagamento_base + pagamento_folga_remunerada) * desconto_transporte /100
        sub_total_quatro= self.parcela_vale

        sub_total_bruto = (sub_total_um  - sub_total_dois - sub_total_tres - sub_total_quatro - faltas_d_s_r)
        
        
        
        
        
        return {
        'sub_total_um': sub_total_um,
        'sub_total_dois': sub_total_dois,
        'sub_total_tres': sub_total_tres,
        'pagamento_base': pagamento_base,
        'pagamento_horas_extras_um': pagamento_horas_extras_um,
        'pagamento_horas_extras_dois': pagamento_horas_extras_dois,
        'pagamento_adicional_noturno': pagamento_adicional_noturno,
        'pagamento_folga_remunerada': pagamento_folga_remunerada,
        'sub_total_quatro': sub_total_quatro,
        'sub_total_dois_onze': sub_total_quatro,
        'sub_total_bruto': sub_total_bruto,
        'empresa_exe': self.empresa_exe,
        'salario_base_mes': salario_base_mes,
        'd_s_r': d_s_r,
        'faltas_d_s_r': faltas_d_s_r,
        'faltas' : faltas,
        'd_s_r_adicionais': d_s_r_adicionais
        
        }        
        
        
