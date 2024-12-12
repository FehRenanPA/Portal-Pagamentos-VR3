import os
import firebase_admin
from firebase_admin import credentials, storage, firestore

# Inicializa o Firebase, mas só se não estiver inicializado
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
            
# Função para fazer upload de arquivos para o Firebase Storage
def upload_file_to_storage(local_file_path, storage_file_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(storage_file_name)
        blob.upload_from_filename(local_file_path)
        print(f"Arquivo {local_file_path} enviado como {storage_file_name}")
    except Exception as e:
        print(f"Erro durante o upload: {e}")

# Função para obter o cliente do Firestore
def get_firestore_client():
    try:
        # A conexão com o Firestore será estabelecida após a inicialização do Firebase
        db = firestore.client()
        print("Conexão com Firestore bem-sucedida.")
        return db
    except Exception as e:
        print(f"Erro ao conectar ao Firestore: {e}")
        return None

# Função para adicionar dados ao Firestore
def add_to_firestore(collection_name, document_id, data):
    firestore_client = get_firestore_client()
    if firestore_client:
        firestore_client.collection(collection_name).document(document_id).set(data)
        print(f"Dados adicionados à coleção {collection_name} com ID {document_id}")
    else:
        print("Erro: não foi possível conectar ao Firestore.")

