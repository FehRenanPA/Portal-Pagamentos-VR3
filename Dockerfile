# Usando uma imagem base do Python mais enxuta
FROM python:3.12-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o container e instalar as dependências Python
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar os arquivos do backend para o diretório de trabalho
COPY functions/Backend /app

# Atualizar pacotes do sistema, instalar dependências necessárias e limpar o cache do apt
RUN apt-get update --fix-missing && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libopenjp2-7-dev \
    libwebp-dev \
    libtiff5-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    gcc \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Pillow para a manipulação de imagens
RUN pip install --no-cache-dir pillow

# Instalar Firebase CLI globalmente
RUN npm install -g firebase-tools

# Copiar os arquivos do Firebase para o container
COPY firebase.json /app/
COPY .firebaserc /app/
COPY functions /app/functions

# Instalar dependências das funções do Firebase
RUN cd /app/functions && npm install

# Expor portas usadas pelos serviços
EXPOSE 5000 
EXPOSE 4000  
EXPOSE 5001 
EXPOSE 8080  
EXPOSE 9099 
EXPOSE 9000  

# Definir o comando padrão para rodar Flask e o Firebase Emulator
CMD ["sh", "-c", "firebase emulators:start --only functions,firestore,auth,storage & python app.py"]
