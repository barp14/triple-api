from flask import Flask
import requests
from pymongo import MongoClient

app = Flask(__name__)

# URL da API de CRM
CRM_API_URL = 'http://localhost:3000/'

# Configuração do MongoDB
client = MongoClient('mongodb+srv://dbuser:DzbX3NP6MySS4ubt@cluster0.8x86g.mongodb.net/?retryWrites=true&w=majority')
db = client['ecommerce']  # Nome do banco de dados
enviados_collection = db['enviados']  # Nova coleção de "enviados"

@app.route('/disparar-email', methods=['POST'])
def disparar_email():
  # Consumindo dados de clientes e campanhas
  clientes = requests.get(CRM_API_URL + 'clientes').json()
  campanhas = requests.get(CRM_API_URL + 'campanhas').json()

  # Simulando o envio de e-mails
  for cliente in clientes:
    for campanha in campanhas:
      print(f'E-mail enviado para: {cliente["email"]} com a campanha {campanha["nome"]}')
            
    # Registrar no banco de dados os e-mails enviados
      enviado = {
          "email": cliente["email"],
          "campanha": campanha["nome"],
          "mensagem": f"Você está recebendo o e-mail da campanha: {campanha['nome']}.",
          "status": "enviado"
      }
      enviados_collection.insert_one(enviado)
            
  return "E-mails disparados com sucesso!"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5001)
