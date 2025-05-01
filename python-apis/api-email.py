from flask import Flask, jsonify
import requests, json

import database
import cache

app = Flask(__name__)
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
          "mensagem": f"Você está recebendo o e-mail da campanha: {campanha['nome']}.",
          "status": "enviado"
      }
    database.enviados_collection.insert_one({**enviado})
    enviados.append(enviado)

  return jsonify(enviados), 200

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
