## 📂 Estrutura de diretórios

- **triple-api/**
  - **python-apis/**
    - `api-crm.py`
    - `api-email.py`
    - `cache.py`
    - `database.py`
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

### 1. Criar o Redis com Docker

```bash
docker run --name redis-container -d -p 6379:6379 redis
```

### 2. Na pasta 'python-apis' importar as dependências do Python

```bash
pip install flask pymongo redis flask-cors
```

### 3. Na pasta 'xlsx-microservice' instalar as dependências do Node

```bash
npm i
```

### 4. Rodar a API CRM (localhost:3000)

```bash
cd python-apis
python api-crm.py
```

### 5. Rodar a API de E-mail (localhost:5000)

```bash
cd python-apis
python api-email.py
```

### 6. Rodar a API de E-mail (localhost:4000)

```bash
cd xlsx-microservice
npm run build
npm start
```


### 7. Rodar o App React (localhost:7000)

```bash
cd frontend
npm start
```

## 👤 Colaboradores

- Barbara Borges Woitas (RGM: 28927940)
- Guilherme Ramos de Oliveira (RGM: 30309751)
- João Adolfo Bonato (RGM: 31338321)
- João Arthur Barp Begnini (RGM: 29462860)
- Vinicius Stadler Ferreira (RGM: 31357652)
