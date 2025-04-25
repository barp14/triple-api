## 🛠️ Como Rodar os Containers

### 1. Criar o Redis com Docker

```bash
docker run --name redis-container -d -p 6379:6379 redis
```

### 2. Rodar a API CRM

```bash
cd crm-api
python crm_api.py
```

### 3. Rodar a API de E-mail

```bash
cd api-email
python email_api.py
```
