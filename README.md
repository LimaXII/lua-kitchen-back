# 🍳 LUA Kitchen — Backend

API local para gerenciamento de receitas, construída com **FastAPI + SQLite**, projetada para uso local sem necessidade de infraestrutura externa.

---

## 🚀 Tecnologias

* Python 3.12+
* FastAPI
* SQLAlchemy
* SQLite
* Poetry

---

## ⚙️ Configuração do ambiente

### 1️⃣ Instalar dependências

```bash
poetry install
```

---

## 🗄️ Inicializar o banco de dados

Cria o banco SQLite e as tabelas.

```bash
poetry run python -m app.database.init_db
```

Após executar, o banco será criado em:

```
app/database/recipes.db
```

---

## ▶️ Rodar a API

```bash
poetry run uvicorn app.main:app --reload
```

A API estará disponível em:

* 👉 http://localhost:8000
* 👉 http://localhost:8000/docs (Swagger)

---

## 👨‍💻 Desenvolvimento

Rodar com reload automático:

```bash
poetry run uvicorn app.main:app --reload
```