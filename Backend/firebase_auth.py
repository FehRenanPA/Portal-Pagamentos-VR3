import os
import json
import pyrebase
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def gerar_id_token():
    try:
        # Carrega o caminho das credenciais do Firebase
        config_path = os.getenv("FIREBASE_CREDENTIALS_PATH2")
        if not config_path:
            raise ValueError("FIREBASE_CREDENTIALS_PATH2 não está definido no arquivo .env")

        # Lê o arquivo de configuração JSON
        with open(config_path, 'r') as f:
            config_cred = json.load(f)

        # Inicializa o Firebase
        firebase = pyrebase.initialize_app(config_cred)
        auth = firebase.auth()

        # Credenciais de login
        email = os.getenv("EMAIL_ADM")
        password =os.getenv("SENHA_ADM")

        # Faz o login e obtém o ID Token
        user = auth.sign_in_with_email_and_password(email, password)
        id_token = user['idToken']
        return id_token  # Retorna o ID Token

    except Exception as e:
        print(f"Erro ao autenticar: {e}")
        return None
