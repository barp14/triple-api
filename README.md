## 📂 Estrutura de diretórios

- **TRIPLE-API/**
  - **crm-api/**
    - `crm.py`
  - **email-api/**
    - `api-email.py`
  - **xlsx-microservice/**
    - **src/**
        - `controller.ts`
        - `redis.ts`
        - `routes.ts`
        - `server.ts`
    - `.env`
    - `package-lock.json`
    - `package.json`
    - `tsconfig.json`
  - **`README.md`**

## 🛠️ Como Rodar a Aplicação

### 1. Na pasta 'triple-api' importar as dependências do Python

```bash
pip install flask pymongo redis
```

### 2. Na pasta 'xlsx-microservice' instalar as dependências do Node

```bash
npm i
```

### 3. Criar o Redis com Docker

```bash
docker run --name redis-container -d -p 6379:6379 redis
```

### 4. Rodar a API CRM

```bash
cd crm-api
python crm.py
```

### 5. Rodar a API de E-mail

```bash
cd api-email
python api-email.py

```
### 6. Rodar a API de E-mail

```bash
cd xlsx-microservice
npm run build
npm start
```

## 👤 Colaboradores

- Barbara Borges Woitas (RGM: 28927940)
- Guilherme Ramos de Oliveira (RGM: 30309751)
- João Adolfo Bonato (RGM: 31338321)
- João Arthur Barp Begnini (RGM: 29462860)
- Vinicius Stadler Ferreira (RGM: 31357652)
