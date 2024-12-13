# Usando uma imagem mais enxuta do Python como base para o app
FROM python:3.10-slim

# Atualizando e instalando dependências adicionais necessárias para compilação
RUN apt-get update && apt-get install -y gcc libffi-dev

# Definindo o diretório de trabalho dentro do contêiner
WORKDIR /functions/Backend

# Copiando o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt .

# Instalando as dependências Python listadas no requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o conteúdo da pasta Backend (onde está o app.py) para o diretório de trabalho
COPY Backend/ /functions/Backend/

# Expondo a porta em que o Flask ou o servidor estará ouvindo
EXPOSE 5000

# Comando para iniciar o app
CMD ["python", "/functions/Backend/app.py"]
