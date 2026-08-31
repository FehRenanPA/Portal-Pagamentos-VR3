import os
import sys

print("cwd:", os.getcwd(), flush=True)
print("arquivo script existe:", os.path.exists("cargo_reembolso_copy.py"), flush=True)

pdf_path = r"C:\Users\felipe.rsantos\Downloads\RELATÓRIO DE LÍQUIDOS FOLHA MENSAL.pdf"
print("pdf existe:", os.path.exists(pdf_path), flush=True)

try:
    import tabula
    import pandas as pd
    print("imports OK", flush=True)

    print("Iniciando leitura do PDF", flush=True)
    dfs = tabula.read_pdf(pdf_path, pages='all')
    print("Tabelas lidas:", len(dfs), flush=True)

    if not dfs:
        raise ValueError("Nenhuma tabela encontrada no PDF")

    df_completo = pd.concat(dfs)
    df_completo.to_csv("folha_completa.csv", index=False)
    print("Arquivo salvo", flush=True)

except Exception as e:
    print("Erro:", type(e).__name__, e, flush=True)
    raise