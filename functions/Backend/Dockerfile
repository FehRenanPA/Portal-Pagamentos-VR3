# Usando uma imagem base do Python
FROM python:3.9-slim

# Diretório de trabalho dentro do container
WORKDIR /app

# Copiar o requirements.txt para dentro do container
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todos os arquivos da aplicação para o container
COPY . .

# Definir a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# Expôr a porta 8080 (port padrão do Flask no Docker)
EXPOSE 8080

# Comando para rodar a aplicação Flask
CMD ["flask", "run"]
