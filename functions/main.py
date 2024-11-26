import firebase_admin
from firebase_admin import credentials, firestore

# Inicia a conexão com o Firebase
cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Conexão com o Firestore
db = firestore.client()

# Função exemplo para adicionar um registro no Firestore
def add_data():
    doc_ref = db.collection('users').document('user1')
    doc_ref.set({
        'name': 'John Doe',
        'age': 30
    })	

