from flask import Flask, jsonify
import requests
from pymongo import MongoClient
import redis
import json

app = Flask(__name__)

CRM_API_URL = 'http://localhost:3000/'

client = MongoClient('mongodb+srv://dbuser:DzbX3NP6MySS4ubt@cluster0.8x86g.mongodb.net/?retryWrites=true&w=majority')
db = client['ecommerce']
enviados_collection = db['enviados'] 

# Configuração do Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

@app.route('/disparar-email', methods=['POST'])
def disparar_email():
	clientes = redis_client.get('clientes')
	campanhas = redis_client.get('campanhas')

	if not clientes:
			clientes = requests.get(CRM_API_URL + 'clientes').json()
			redis_client.set('clientes', json.dumps(clientes), ex=300)  # Cache por 5 minutos
	else:
			clientes = json.loads(clientes)

	if not campanhas:
			campanhas = requests.get(CRM_API_URL + 'campanhas').json()
			redis_client.set('campanhas', json.dumps(campanhas), ex=300)  # Cache por 5 minutos
	else:
			campanhas = json.loads(campanhas)

	enviados_collection.delete_many({}) # Deleta tudo que já foi enviado antes de enviar novamente para não sobrecarregar o banco de dados

	for cliente in clientes:
			for campanha in campanhas:
					enviado = {
							"email": cliente["email"],
							"campanha": campanha["nome"],
							"mensagem": f"Você está recebendo o e-mail da campanha: {campanha['nome']}.",
							"status": "enviado"
					}
					enviados_collection.insert_one(enviado)

	enviados = list(enviados_collection.find({}, {"_id": 0}))  # Ignora o _id para facilitar o JSON

	return jsonify(enviados), 200

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)
