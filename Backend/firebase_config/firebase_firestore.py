import os
import firebase_admin
from firebase_admin import credentials, firestore, auth
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def initialize_firebase():
    # Obter o caminho para o arquivo de credenciais a partir do .env
    cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
    if not cred_path or not os.path.exists(cred_path):
        raise FileNotFoundError("Arquivo de credenciais do Firebase não encontrado. Verifique o caminho em .env")
    
    # Inicializar o Firebase Admin SDK
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Função para acessar o Firestore
def get_firestore_client():
    try:
        return firestore.client()
    except Exception as e:
        raise RuntimeError(f"Erro ao acessar o Firestore: {e}")

# Função para verificar o token de um usuário
def verify_user_token(id_token):
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token  # Retorna as informações do usuário
    except auth.InvalidIdTokenError:
        return {"error": "Token inválido."}
    except auth.ExpiredIdTokenError:
        return {"error": "Token expirado."}
    except auth.RevokedIdTokenError:
        return {"error": "Token revogado."}
    except Exception as e:
        return {"error": f"Erro ao verificar o token: {e}"}

# Exemplo de uso
if __name__ == "__main__":
    try:
        initialize_firebase()
        print("Firebase inicializado com sucesso!")

        # Obter cliente do Firestore
        firestore_client = get_firestore_client()
        print("Conexão com Firestore estabelecida.")

        # Exemplo de verificação de token (substitua por um token válido para testar)
        test_token = "SEU_ID_TOKEN_AQUI"
        user_data = verify_user_token(test_token)
        print("Dados do usuário:", user_data)
    except Exception as e:
        print(f"Erro ao inicializar o Firebase: {e}")
    