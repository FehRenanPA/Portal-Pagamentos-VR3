import firebase_admin
from firebase_admin import credentials, storage, firestore

# Inicializa o Firebase, mas só se não estiver inicializado
def initialize_firebase():
    try:
        # Verifica se o Firebase já foi inicializado
        if not firebase_admin._apps:
            cred = credentials.Certificate(
                r"C:\Users\felipe.rsantos\Downloads\Projeto Recibos\PORTAL DE PAGAMENTOS CONSTRUMAQ\Backend\serviceAccountKey.json"
            )
            firebase_admin.initialize_app(cred, {
                "storageBucket": "portal-pagamento-vr3.firebasestorage.app"
            })
        else:
            print("Firebase já foi inicializado.")
    except ValueError as e:
        print(f"Erro ao inicializar o Firebase: {e}")

# Função para fazer upload de arquivos para o Firebase Storage
def upload_file_to_storage(local_file_path, storage_file_name):
    try:
        bucket = storage.bucket()
        blob = bucket.blob(storage_file_name)
        blob.upload_from_filename(local_file_path)
        print(f"Arquivo {local_file_path} enviado como {storage_file_name}")
    except Exception as e:
        print(f"Erro durante o upload: {e}")

# Função para acessar o Firestore
def get_firestore_client():
    try:
        db = firestore.client()
        print("Conexão com Firestore bem-sucedida.")
        return db
    except Exception as e:
        print(f"Erro ao conectar ao Firestore: {e}")
        return None
