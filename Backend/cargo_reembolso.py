

class FuncionarioReembolso:

    def __init__(self, name, nome_funcao,equipe, numero_cpf, chave_pix,valor_hora_base, valor_adicional_noturno, valor_hora_extra_um,
    valor_hora_extra_dois, valor_repouso_remunerado,valor_ferias, valor_um_terco_ferias, valor_decimo_terceiro, valor_antecipa_salario, 
    pagamento_fgts, desconto_inss, desconto_refeicao, desconto_transporte, empresa, cnpj_empresa, salario_base):
        self.name = name
        self.nome_funcao= nome_funcao
        self.equipe=equipe
        self.numero_cpf= numero_cpf
        self.chave_pix = chave_pix
        self.valor_hora_base = valor_hora_base
        self.valor_repouso_remunerado = valor_repouso_remunerado
        self.valor_hora_extra_um = valor_hora_extra_um
        self.valor_hora_extra_dois = valor_hora_extra_dois
        self.valor_adicional_noturno = valor_adicional_noturno 
        self.valor_ferias=valor_ferias
        self.valor_um_terco_ferias=valor_um_terco_ferias
        self.valor_decimo_terceiro=valor_decimo_terceiro
        self.valor_antecipa_salario=valor_antecipa_salario
        self.pagamento_fgts=pagamento_fgts
        self.desconto_inss=desconto_inss
        self.desconto_refeicao=desconto_refeicao
        self.desconto_transporte=desconto_transporte
        self.empresa=empresa
        self.cnpj_empresa=cnpj_empresa
        self.salario_base = salario_base
        
        
    def to_dict(self):
        return {
            'numero_cpf': self.numero_cpf,
            'chave_pix': self.chave_pix,
            'valor_hora_base': self.valor_hora_base,
            'valor_hora_extra_um': self.valor_hora_extra_um,
            'valor_hora_extra_dois': self.valor_hora_extra_dois,
            'adicional_noturno': self.valor_adicional_noturno,
            'repouso_remunerado': self.valor_repouso_remunerado,
            'valor_ferias': self.valor_ferias,
            'valor_um_terco_ferias': self.valor_um_terco_ferias,
            'valor_decimo_terceiro': self.valor_decimo_terceiro,
            'valor_antecipa_salario': self.valor_antecipa_salario,
            'pagamento_fgts': self.pagamento_fgts,
            'desconto_inss': self.desconto_inss,
            'desconto_refeicao': self.desconto_refeicao,
            'desconto_transporte': self.desconto_transporte,
            'empresa': self.empresa,
            'cnpj_empresa': self.cnpj_empresa,
            'salario_base': self.salario_base  # Exemplo de cálculo de salário base
        }
    
   

def __repr__(self):
        return (f"Funcionario(nome='{self.nome}', nome_funcao'{self.nome_funcao}', equipe'{self.equipe}', numero_cpf='{self.numero_cpf}', chave_pix='{self.chave_pix}', valor_hora_base={self.valor_hora_base}, "
            f"repouso_remunerado={self.valor_repouso_remunerado}, valor_hora_extra_um={self.valor_hora_extra_um}, "
            f"valor_hora_extra_dois={self.valor_hora_extra_dois}, adicional_noturno={self.valor_adicional_noturno}, "
            f"valor_ferias={self.valor_ferias}, valor_um_terco_ferias={self.valor_um_terco_ferias}, "
            f"valor_decimo_terceiro={self.valor_decimo_terceiro}, valor_antecipa_salario={self.valor_antecipa_salario}, "
            f"pagamento_fgts={self.pagamento_fgts}, desconto_inss={self.desconto_inss}, "
            f"desconto_refeicao={self.desconto_refeicao}, desconto_transporte={self.desconto_transporte}), empresa={self.empresa}, "
            f"cnpj_empresa={self.cnpj_empresa}, salario_base={self.salario_base})")


