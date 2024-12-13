# Imagem base com Node.js e Python
FROM node:20-buster

# Instalar o Python e dependências do sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Definir o diretório de trabalho no container
WORKDIR /app

# Copiar os arquivos do projeto para dentro do container
COPY . .

# Instalar dependências do Node.js
RUN npm install

# Instalar dependências do Python (se necessário)
RUN pip3 install -r Backend/requirements.txt

# Expor a porta que o Flask vai usar (geralmente 5000)
EXPOSE 5000

# Comando para rodar a função do Firebase
CMD ["firebase", "emulators:start", "--only", "functions"]
