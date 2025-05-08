# database.py
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId

_MONGO_URI = 'mongodb+srv://dbuser:DzbX3NP6MySS4ubt@cluster0.8x86g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'

client = MongoClient(_MONGO_URI)
db = client['ecommerce']
clientes_collection = db['clientes']
campanhas_collection = db['campanhas']
enviados_collection = db['enviados']

def ping():
	try:
		client.admin.command('ping')
		print("Conexão com MongoDB bem-sucedida!")
	except ConnectionFailure as e:
		print(f"Falha ao conectar ao MongoDB: {e}")
	except Exception as e:
		print(f"Erro inesperado ao tentar conectar: {e}")

def serialize_objectid(obj):
	if isinstance(obj, ObjectId):
		return str(obj)
	raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")
