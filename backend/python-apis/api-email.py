import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mail import Mail, Message
from http import HTTPStatus
import requests

import database
import cache

# carrega o .env
load_dotenv()

app = Flask(__name__)
CORS(app)
database.ping()

# --- CONFIGURAÇÃO SMTP via .env ---
app.config.update(
    MAIL_SERVER=os.getenv('MAIL_SERVER'),
    MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
    MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True') == 'True',
    MAIL_USERNAME=os.getenv('MAIL_USERNAME'),
    MAIL_PASSWORD=os.getenv('MAIL_PASSWORD'),
    MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
)
mail = Mail(app)

CRM_API_URL = os.getenv('CRM_API_URL', 'http://localhost:3000/')

@app.route('/disparar-email', methods=['POST'])
def disparar_email():
    clientes = cache.get('clientes') or requests.get(f'{CRM_API_URL}clientes').json()
    cache.set('clientes', clientes)

    campanhas = cache.get('campanhas') or requests.get(f'{CRM_API_URL}campanhas').json()
    cache.set('campanhas', campanhas)

    database.enviados_collection.delete_many({})

    enviados = []
    for cliente in clientes:
        destinatario = cliente['email']
        for campanha in campanhas:
            assunto = f"Campanha: {campanha['nome']}"
            corpo = (
                f"Olá {cliente.get('nome','')},\n\n"
                f"Você está recebendo este e-mail sobre a campanha “{campanha['nome']}”.\n"
                "Obrigado pelo seu interesse!"
            )
            msg = Message(subject=assunto, recipients=[destinatario], body=corpo)

            try:
                mail.send(msg)
                status = 'enviado'
            except Exception as e:
                status = 'erro'
                error_msg = str(e)
                app.logger.error(f'Falha ao enviar para {destinatario}: {error_msg}')

            registro = {
                "email": destinatario,
                "campanha": campanha['nome'],
                "campanhatag": campanha['tag'],
                "status": status
            }
            result = database.enviados_collection.insert_one(registro)
            registro["_id"] = database.serialize_objectid(result.inserted_id)
            enviados.append(registro)

    return jsonify(enviados), HTTPStatus.OK

@app.route('/disparar-email-by-tag', methods=['POST'])
def disparar_email_by_tag():
    campanhatag = request.args.get('campanhatag')
    if not campanhatag:
        return jsonify({"error": "campanhatag é obrigatória"}), HTTPStatus.BAD_REQUEST

    clientes = cache.get('clientes') or requests.get(f'{CRM_API_URL}clientes').json()
    cache.set('clientes', clientes)

    campanhas = cache.get('campanhas') or requests.get(f'{CRM_API_URL}campanhas').json()
    cache.set('campanhas', campanhas)

    campanhas_filtradas = [c for c in campanhas if c['tag'] == campanhatag]
    if not campanhas_filtradas:
        return jsonify({"error": f"Nenhuma campanha encontrada com a tag '{campanhatag}'"}), HTTPStatus.NOT_FOUND

    enviados = []
    for cliente in clientes:
        destinatario = cliente['email']
        for campanha in campanhas_filtradas:
            assunto = f"Campanha: {campanha['nome']}"
            corpo = (
                f"Olá {cliente.get('nome','')},\n\n"
                f"Você está recebendo este e-mail sobre a campanha “{campanha['nome']}”."
            )
            msg = Message(subject=assunto, recipients=[destinatario], body=corpo)

            try:
                mail.send(msg)
                status = 'enviado'
            except Exception as e:
                status = 'erro'
                app.logger.error(f'Falha ao enviar para {destinatario}: {e}')

            registro = {
                "email": destinatario,
                "campanha": campanha['nome'],
                "campanhatag": campanha['tag'],
                "status": status
            }
            result = database.enviados_collection.insert_one(registro)
            registro["_id"] = database.serialize_objectid(result.inserted_id)
            enviados.append(registro)

    return jsonify(enviados), HTTPStatus.OK

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
