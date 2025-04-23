from flask import Flask
import requests

app = Flask(__name__)

# URL da api de CRM
CRM_API_URL = 'http://crm-api-container:3000/'

@app.route('/disparar-email', methods=['POST'])
def disparar_email():
  # Consumindo dados de clientes e campanhas
  clientes = requests.get(CRM_API_URL + 'clientes').json()
  campanhas = requests.get(CRM_API_URL + 'campanhas').json()

  # Simulando o envio de e-mails
  for cliente in clientes:
    for campanha in campanhas:
      print(f'E-mail enviado para: {cliente["email"]} com a campanha {campanha["nome"]}')
            
  return "E-mails disparados com sucesso!"

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
	