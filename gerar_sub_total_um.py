from criar_cargo import CriarFuncionario
import logging




funcionario_dict = CriarFuncionario.carregar_funcionarios()


# Valida se os dados foram carregados corretamente
class Sub_total_um:

    def __init__(self, nome_cargo, name_funcionario,data_inicio,data_fim,data_pagamento):
        self.nome_cargo= nome_cargo
        self.name_funcionario = name_funcionario
        self.data_inicio= data_inicio
        self.data_fim= data_fim
        self.data_pagamento = data_pagamento
        self.horas_trabalhadas = 0
        self.horas_extras_um = 0
        self.horas_extras_dois = 0
        self.horas_noturnas = 0
        self.repouso_remunerado = 7.33
        self.valor_ferias = 0
        self.correcao_positiva = 0
        self.correcao_negativa = 0
        self.parcela_vale=0
        self.valor_diarias = 0
        self.mais = 0
        self.menos = 0
        self.diferenca_calculo = 0
      

        
        

    
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
        
    def adicionar_correcao_positiva(self,valor):
        self.correcao_positiva += valor        
        
    def adicionar_correcao_negativa(self,valor):
       self.correcao_negativa += valor  
        
    def adicionar_valor_por_hora(self,valor):    
        self.valor_diarias += valor
               
    def adicionar_pagamento_vale(self,valor):    
        self.parcela_vale += valor
        
    def adicionar_diferenca_positiva(self,valor):    
        self.diferenca_calculo += valor    
        
    def valida_funcionario(self):
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
        valor_ferias = self.funcionario['valor_ferias']
        valor_antecipa_ferias = self.funcionario['valor_um_terco_ferias']
        valor_decimo_terceito = self.funcionario['valor_decimo_terceiro']
        pagamento_fgts = self.funcionario['pagamento_fgts']
        desconto_inss = self.funcionario['desconto_inss']
        desconto_refeicao =self.funcionario['desconto_refeicao']
        desconto_transporte = self.funcionario['desconto_transporte']
        
            
        #SUB-TATAL 1
        pagamento_base = self.horas_trabalhadas * valor_hora_base
        pagamento_horas_extras_um = self.horas_extras_um * valor_hora_extra_um
        pagamento_horas_extras_dois = self.horas_extras_dois * valor_hora_extra_dois
        pagamento_adicional_noturno = self.horas_noturnas * adicional_noturno
        
        if self.horas_trabalhadas < 44 :
           self.repouso_remunerado = 0
            

        pagamento_folga_remunerada = self.repouso_remunerado * valor_repouso_remunerado
        
    
        
        sub_total_um = (pagamento_base + 
                        pagamento_horas_extras_um +
                        pagamento_horas_extras_dois +
                        pagamento_adicional_noturno + 
                        pagamento_folga_remunerada) 
        #SUB-TOTAL 2
        sub_total_um_um = sub_total_um * valor_ferias /100
        sub_total_um_dois = sub_total_um* valor_antecipa_ferias /100 #1/3 ferias
        sub_total_um_tres = sub_total_um * valor_decimo_terceito /100
        #sub_total_um_quantro =  self.adiantamento_sal * valor_antecipa_salario #
        sub_total_um_cinco = sub_total_um  * (pagamento_fgts /100)
        
        sub_total_dois =(sub_total_um + sub_total_um_um + sub_total_um_dois + sub_total_um_tres+ sub_total_um_cinco)
        
        #SUB-TOTAL 3
        
        sub_total_dois_seis = sub_total_dois * (desconto_inss/100)
        sub_total_dois_sete = (pagamento_base + pagamento_folga_remunerada) * desconto_refeicao/100
        sub_total_dois_oito = (pagamento_base + pagamento_folga_remunerada) * desconto_transporte /100
        
        ##Calculo par somar ou subtrair a correção
        sub_total_int = sub_total_dois
        
        if self.valor_diarias == 0:
            self.mais = 0
            self.menos = 0
       
        elif sub_total_int < self.valor_diarias:
            self.mais = self.valor_diarias - sub_total_int
            self.menos=0
            
            
        elif sub_total_int > self.valor_diarias:
            self.menos = sub_total_int - self.valor_diarias
            self.mais=0 
            
          
        sub_total_dois_nove = self.correcao_positiva + self.mais 
        sub_total_dois_dez =  self.correcao_negativa + self.menos 
        sub_total_dois_onze = self.parcela_vale
        sub_total_dois_treze = self.diferenca_calculo
        sub_total_bruto = (sub_total_dois - sub_total_dois_seis - sub_total_dois_sete - sub_total_dois_oito + sub_total_dois_nove - sub_total_dois_dez + sub_total_dois_treze)
        
        
        
       
        sub_total_tres =( sub_total_bruto - sub_total_dois_onze)
        
        
        
        
        return {
        'sub_total_um': sub_total_um,
        'sub_total_dois': sub_total_dois,
        'sub_total_tres': sub_total_tres,
        'pagamento_base': pagamento_base,
        'pagamento_horas_extras_um': pagamento_horas_extras_um,
        'pagamento_horas_extras_dois': pagamento_horas_extras_dois,
        'pagamento_adicional_noturno': pagamento_adicional_noturno,
        'pagamento_folga_remunerada': pagamento_folga_remunerada,
        'sub_total_um_um' : sub_total_um_um,
        'sub_total_um_dois' : sub_total_um_dois,
        'sub_total_um_tres' : sub_total_um_tres,
        'sub_total_um_cinco' : sub_total_um_cinco,
        'sub_total_dois_seis' : sub_total_dois_seis,
        'sub_total_dois_sete' : sub_total_dois_sete,
        'sub_total_dois_oito' : sub_total_dois_oito,
        'sub_total_dois_nove' : sub_total_dois_nove,
        'sub_total_dois_dez' : sub_total_dois_dez,
        'sub_total_dois_onze' : sub_total_dois_onze,
        'sub_total_dois_treze' : sub_total_dois_treze,
        'sub_total_bruto': sub_total_bruto,
        
        
        
}