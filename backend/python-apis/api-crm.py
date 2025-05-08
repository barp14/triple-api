from flask import Flask, jsonify, request
from http import HTTPStatus
from flask_cors import CORS

import database
import cache

app = Flask(__name__)
CORS(app)  # Permite CORS para todas as origens
database.ping()

@app.route('/clientes', methods=['GET'])
def buscar_clientes():

  # bate no cache
  data = cache.get('clientes')

  if data is None:
    # busca os clientes no banco
    raw = list(database.clientes_collection.find())

    data = [
      {**cliente, '_id': database.serialize_objectid(cliente['_id'])}
      for cliente in raw
    ]
    cache.set('clientes', data)

  return jsonify(data), HTTPStatus.OK

@app.route('/clientes', methods=['POST'])
def criar_cliente():

  payload = request.get_json()

  if isinstance(payload, list):
    if not all('nome' in c and 'email' in c for c in payload):
      return jsonify({'message': 'Nome e email são obrigatórios'}), HTTPStatus.BAD_REQUEST
    result = database.clientes_collection.insert_many(payload)

    # Serializa objetos inseridos
    inserted = []

    for doc, oid in zip(payload, result.inserted_ids):
      inserted.append({**doc, '_id': database.serialize_objectid(oid)})
    else:
      if 'nome' not in payload or 'email' not in payload:
        return jsonify({'message': 'Nome e email são obrigatórios'}), HTTPStatus.BAD_REQUEST
      
  result = database.clientes_collection.insert_one(payload)
  inserted = [{**payload, '_id': database.serialize_objectid(result.inserted_id)}]

  cache.invalidate('clientes')

  return jsonify(inserted), HTTPStatus.CREATED

@app.route('/campanhas', methods=['GET'])
def buscar_campanhas():

  # bate no cache
  data = cache.get('campanhas')

  if data is None:
    # busca as campanhas no banco
    raw = list(database.campanhas_collection.find())

    data = [
      {**campanha, '_id': database.serialize_objectid(campanha['_id'])}
      for campanha in raw
    ]
    cache.set('campanha', data)

  return jsonify(data), HTTPStatus.OK

@app.route('/campanhas', methods=['POST'])
def criar_campanha():

  payload = request.get_json()

  if isinstance(payload, list):
    if not all('nome' in c and 'tag' in c for c in payload):
      return jsonify({'message': 'Nome e tag são obrigatórios'}), HTTPStatus.BAD_REQUEST
    result = database.campanhas_collection.insert_many(payload)

    # Serializa objetos inseridos
    inserted = []

    for doc, oid in zip(payload, result.inserted_ids):
      inserted.append({**doc, '_id': database.serialize_objectid(oid)})
    else:
      if 'nome' not in payload or 'tag' not in payload:
        return jsonify({'message': 'Nome e tag são obrigatórios'}), HTTPStatus.BAD_REQUEST
      
  result = database.campanhas_collection.insert_one(payload)
  inserted = [{**payload, '_id': database.serialize_objectid(result.inserted_id)}]

  cache.invalidate('campanhas')

  return jsonify(inserted), HTTPStatus.CREATED

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3000)
