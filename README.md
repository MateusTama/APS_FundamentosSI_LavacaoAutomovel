# 🚀 Projeto Flask

Este é um projeto desenvolvido com [Flask](https://flask.palletsprojects.com/) utilizando Python 3.10.5, ambiente virtual e variáveis de ambiente definidas em um arquivo `config.env`.

## ✅ Requisitos

- Python 3.10.5 instalado
- pip (gerenciador de pacotes do Python)
- Git (opcional)

---

## ⚙️ Passo a passo para executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/MateusTama/APS_FundamentosSI_LavacaoAutomovel.git
```

### 2. Crie e ative o ambiente virtual

**Linux/macOS:**
```bash
python3.10 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados PostgreSQL

Certifique-se de que o PostgreSQL está instalado e rodando. Em seguida, crie um banco de dados e um usuário com permissões adequadas.

Exemplo com psql:

```sql
CREATE DATABASE nome_do_banco;
```

### 5. Crie o arquivo `config.env`

Na raiz do projeto, crie um arquivo chamado `config.env` com o seguinte conteúdo:

```ini
DB_DATABASE=nome_do_banco
DB_USER=usuario
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=sua_chave_secreta
```

⚠️ **Importante:** este arquivo **NÃO deve ser versionado**. Adicione `config.env` ao `.gitignore`.

---

### 6. Execute a aplicação Flask

```bash
flask run
```

Por padrão, a aplicação estará disponível em:  
🔗 http://127.0.0.1:5000

---

## 📁 Estrutura resumida do projeto

```
.
├── models/
│   ├── __init__.py
│   ├── routes.py
│   └── ...
├── config.env
├── requirements.txt
├── app.py
├── .gitignore
└── README.md
```

---
