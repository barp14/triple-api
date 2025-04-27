from flask import Flask, jsonify, request
from http import HTTPStatus
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from bson import ObjectId
import redis
import json

app = Flask(__name__)

client = MongoClient('mongodb+srv://dbuser:DzbX3NP6MySS4ubt@cluster0.8x86g.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['ecommerce'] 
clientes_collection = db['clientes'] 
campanhas_collection = db['campanhas']

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

# Função para converter ObjectId para string para que o Python consiga serializar esse tipo para JSON.
def serialize_objectid(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

# Teste de conexão com o MongoDB
try:
    client.admin.command('ping')
    print("Conexão com MongoDB bem-sucedida!")
except ConnectionFailure as e:
    print(f"Falha ao conectar ao MongoDB: {e}")
except Exception as e:
    print(f"Erro inesperado ao tentar conectar: {e}")

@app.route('/clientes', methods=['GET'])
def buscar_clientes():
    # Verificar cache no Redis
    clientes = redis_client.get('clientes')
    if not clientes:
        clientes = list(clientes_collection.find())
        serialized_clientes = [{**cliente, '_id': serialize_objectid(cliente['_id'])} for cliente in clientes]
        redis_client.set('clientes', json.dumps(serialized_clientes), ex=300)  # Cache por 5 minutos
    else:
        serialized_clientes = json.loads(clientes)
    return jsonify(serialized_clientes), HTTPStatus.OK

@app.route('/campanhas', methods=['GET'])
def buscar_campanhas():
    # Verificar cache no Redis
    campanhas = redis_client.get('campanhas')
    if not campanhas:
        campanhas = list(campanhas_collection.find()) 
        serialized_campanhas = [{**campanha, '_id': serialize_objectid(campanha['_id'])} for campanha in campanhas]
        redis_client.set('campanhas', json.dumps(serialized_campanhas), ex=300)  # Cache por 5 minutos
    else:
        serialized_campanhas = json.loads(campanhas)
    return jsonify(serialized_campanhas), HTTPStatus.OK

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.get_json()

    if isinstance(data, list):  # Verifica se é uma lista de clientes
        if not all('nome' in cliente and 'email' in cliente for cliente in data):
            return jsonify({'message': 'Nome e email são obrigatórios'}), HTTPStatus.BAD_REQUEST
        
        try:
            clientes_collection.insert_many(data)  # Inserir múltiplos clientes de uma vez
            redis_client.delete('clientes')  # Limpar cache
            serialized_data = [dict(cliente, **{'_id': serialize_objectid(cliente['_id'])}) for cliente in data]
            return jsonify(serialized_data), HTTPStatus.CREATED
        except Exception as e:
            return jsonify({'message': f'Erro ao inserir dados: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        if 'nome' not in data or 'email' not in data:
            return jsonify({'message': 'Nome e email são obrigatórios'}), HTTPStatus.BAD_REQUEST
        
        try:
            cliente_inserido = clientes_collection.insert_one(data)  # Inserir um único cliente
            redis_client.delete('clientes')  # Limpar cache
            serialized_data = dict(data, **{'_id': serialize_objectid(cliente_inserido.inserted_id)})
            return jsonify(serialized_data), HTTPStatus.CREATED
        except Exception as e:
            return jsonify({'message': f'Erro ao inserir dados: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/campanhas', methods=['POST'])
def criar_campanha():
    data = request.get_json()

    if isinstance(data, list):  # Verifica se é uma lista de campanhas
        if not all('nome' in campanha for campanha in data):
            return jsonify({'message': 'Nome da campanha é obrigatório'}), HTTPStatus.BAD_REQUEST
        
        try:
            campanhas_collection.insert_many(data)  # Inserir múltiplas campanhas
            redis_client.delete('campanhas')  # Limpar cache
            serialized_data = [
                {**campanha, '_id': serialize_objectid(campanha['_id'])} for campanha in data
            ]
            return jsonify(serialized_data), HTTPStatus.CREATED
        except Exception as e:
            return jsonify({'message': f'Erro ao inserir dados: {str(e)}'}), HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        if 'nome' not in data:
            return jsonify({'message': 'Nome da campanha é obrigatório'}), HTTPStatus.BAD_REQUEST
        
        nova_campanha = {
            'nome': data['nome']
        }
        
        campanhas_collection.insert_one(nova_campanha)
        redis_client.delete('campanhas')  # Limpar cache
        serialized_campanha = {**nova_campanha, '_id': serialize_objectid(nova_campanha['_id'])}
        return jsonify(serialized_campanha), HTTPStatus.CREATED

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
