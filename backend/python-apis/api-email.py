from flask import Flask, request, jsonify
import requests, json
from flask_cors import CORS

import database
import cache

app = Flask(__name__)
CORS(app)
database.ping()

CRM_API_URL = 'http://localhost:3000/'

@app.route('/disparar-email', methods=['POST'])
def disparar_email():
  clientes = cache.get('clientes')
  if clientes is None:
    clientes = requests.get(f'{CRM_API_URL}clientes').json()
    cache.set('clientes', clientes)

  campanhas = cache.get('campanhas')
  if campanhas is None:
    campanhas = requests.get(f'{CRM_API_URL}campanhas').json()
    cache.set('campanhas', campanhas)

  # limpa envios antigos
  database.enviados_collection.delete_many({})

  enviados = []
  for cliente in clientes:
    for campanha in campanhas:
      enviado = {
        "email": cliente["email"],
        "campanha": campanha["nome"],
        "campanhatag": campanha["tag"],
        "mensagem": f"Você está recebendo o e-mail da campanha: {campanha['nome']}."
      }
      database.enviados_collection.insert_one({**enviado})
      enviados.append(enviado)

  return jsonify(enviados), 200

@app.route('/disparar-email-by-tag', methods=['POST'])
def disparar_email_by_tag():
  campanhatag = request.args.get('campanhatag') # http://localhost:5000/disparar-email-by-tag?campanhatag={campanhatag}

  if not campanhatag:
    return jsonify({"error": "campanhatag é obrigatória"}), 400

  clientes = cache.get('clientes')
  if clientes is None:
    clientes = requests.get(f'{CRM_API_URL}clientes').json()
    cache.set('clientes', clientes)

  campanhas = cache.get('campanhas')
  if campanhas is None:
    campanhas = requests.get(f'{CRM_API_URL}campanhas').json()
    cache.set('campanhas', campanhas)

  # Filtrar campanhas pela campanhatag passada
  campanhas_filtradas = [campanha for campanha in campanhas if campanha['tag'] == campanhatag]

  if not campanhas_filtradas:
    return jsonify({"error": f"Nenhuma campanha encontrada com a tag '{campanhatag}'"}), 404

  # database.enviados_collection.delete_many({})

  enviados = []
  for cliente in clientes:
    for campanha in campanhas_filtradas:
      enviado = {
        "email": cliente["email"],
        "campanha": campanha["nome"],
        "campanhatag": campanha["tag"],
        "mensagem": f"Você está recebendo o e-mail da campanha: {campanha['nome']}."
      }
      database.enviados_collection.insert_one({**enviado})
      enviados.append(enviado)

  return jsonify(enviados), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
