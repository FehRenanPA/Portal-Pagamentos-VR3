import os
import firebase_admin
from firebase_admin import credentials, storage, firestore

def initialize_firebase():
    try:
        if not firebase_admin._apps:
            # Usando caminho relativo para o arquivo de credenciais
            cred_path = os.path.join(os.getcwd(), "Backend", "serviceAccountKey.json")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred, {
                "storageBucket": "portal-pagamento-vr3.appspot.com"
            })
            print("Firebase inicializado com sucesso.")
        else:
            print("Firebase já foi inicializado.")
    except ValueError as e:
        print(f"Erro ao inicializar o Firebase: {e}")
    except FileNotFoundError as e:
        print(f"Arquivo de credenciais não encontrado: {e}")
    except Exception as e:
        print(f"Erro inesperado ao inicializar o Firebase: {e}")
