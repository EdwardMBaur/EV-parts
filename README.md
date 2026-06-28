# EV.parts — Back-end API

Marketplace de Peças para Veículos Elétricos | Projeto de Desenvolvimento Web  
**Edward Marzon Baur · Giovane William Budal**

---

## Stack

| Camada | Tecnologia |
|--------|-----------|
| Framework API | **FastAPI** (Python 3.12) |
| Banco de Dados | **NeonDB** (PostgreSQL 16 serverless) |
| ORM | **SQLAlchemy 2** |
| Migrations | **Alembic** |
| Autenticação | **JWT** (python-jose + passlib/bcrypt) |
| Containerização | **Docker** (só a API — banco fica no Neon) |
| CEP | **ViaCEP** (gratuito, sem chave) |

---

## Configurando o NeonDB

### 1. Crie o projeto no Neon

1. Acesse [console.neon.tech](https://console.neon.tech) e crie uma conta gratuita.
2. Clique em **"New Project"** → dê um nome (ex: `evparts`).
3. Escolha a região mais próxima (ex: `South America (São Paulo)` se disponível, ou `US East`).
4. Clique em **"Create Project"**.

### 2. Obtenha a connection string

No painel do projeto:
- Vá em **"Connection Details"**
- Selecione **"Connection string"** e o driver **"psycopg2"**
- Copie a URL — ela tem este formato:

```
postgresql+psycopg2://USER:PASS@ep-cool-name-123456.us-east-2.aws.neon.tech/evparts?sslmode=require
```

> **Dica de produção:** use a URL do **pooler (PgBouncer)** — troca `.neon.tech` por `-pooler.us-east-2.aws.neon.tech`.  
> O pooler gerencia conexões eficientemente e é recomendado para APIs em produção.

### 3. Configure o .env

```bash
cp .env.example .env
```

Edite `.env` e cole sua connection string:

```env
DATABASE_URL=postgresql+psycopg2://USER:PASS@ep-xxx.us-east-2.aws.neon.tech/evparts?sslmode=require
SECRET_KEY=gere_com__python_-c_"import_secrets;_print(secrets.token_hex(32))"
APP_ENV=development
```

---

## Como rodar

### Com Docker (recomendado)

```bash
# 1. Configurar variáveis
cp .env.example .env
# editar .env com sua DATABASE_URL do Neon

# 2. Subir a API
docker compose up --build

# 3. Rodar migrations no Neon
docker compose exec api alembic upgrade head

# 4. Popular dados iniciais
docker compose exec api python -m app.seed
```

API disponível em **http://localhost:8000**  
Documentação interativa: **http://localhost:8000/docs**

### Sem Docker (local direto)

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # preencher DATABASE_URL

alembic upgrade head
python -m app.seed
uvicorn app.main:app --reload
```

---

## Usuário admin padrão (após seed)

| Campo | Valor |
|-------|-------|
| Email | `admin@evparts.com.br` |
| Senha | `Admin@123` |

---

## Estrutura do Projeto

```
ev-parts-backend/
├── app/
│   ├── main.py                      # FastAPI app, CORS, routers
│   ├── config.py                    # Settings via pydantic-settings
│   ├── database.py                  # Engine NeonDB + pool serverless
│   ├── seed.py                      # Categorias, veículos, admin
│   ├── models/                      # SQLAlchemy ORM (espelho do ERD)
│   │   ├── usuario.py
│   │   ├── endereco.py
│   │   ├── categoria.py
│   │   ├── veiculo.py
│   │   ├── peca.py
│   │   ├── compatibilidade.py       # Matriz peça × veículo
│   │   ├── pedido.py
│   │   ├── item_pedido.py
│   │   └── pagamento.py
│   ├── schemas/                     # Pydantic request/response
│   ├── routers/                     # Endpoints
│   │   ├── auth.py                  # RF02 Cadastro · RF03 Login
│   │   ├── usuarios.py
│   │   ├── enderecos.py             # RF02 busca CEP (ViaCEP)
│   │   ├── categorias.py            # RF01 Categorias em destaque
│   │   ├── veiculos.py
│   │   ├── pecas.py                 # RF04 Catálogo · RF05 Detalhes
│   │   ├── pedidos.py               # RF05 Checkout
│   │   ├── pagamentos.py            # RF05 Cartão/Pix/Boleto + webhook
│   │   └── logistica.py             # RF05 Calculadora de frete
│   ├── services/
│   │   ├── cep_service.py           # Integração ViaCEP
│   │   ├── compatibilidade_service.py
│   │   └── frete_service.py         # Motor logístico ADR
│   └── core/
│       ├── security.py              # JWT, bcrypt
│       └── dependencies.py          # get_current_user, guards
├── alembic/                         # Migrations
├── docker-compose.yml               # Só a API (banco = Neon)
├── Dockerfile
├── requirements.txt
└── .env.example
```

---

## Endpoints

### Autenticação
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/auth/cadastro` | RF02 — Cadastro (Comprador/Oficina/Fornecedor) |
| `POST` | `/auth/login` | RF03 — Login via e-mail ou CPF/CNPJ |

### Catálogo (RF04)
| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/pecas/?vin=9BWZ...` | Busca inteligente com filtros |
| `GET` | `/pecas/{id}` | RF05 — Detalhes + ficha técnica |
| `POST` | `/pecas/compatibilidade/verificar` | Verifica se peça serve no veículo |
| `GET` | `/categorias/` | RF01 — Categorias com contagem de peças |
| `GET` | `/veiculos/?montadora=VW` | Autocompletar seletor de veículo |

### Logística (RF05)
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/logistica/frete` | Calcula frete (detecta carga ADR) |
| `GET` | `/logistica/frete/peca/{id}?cep_destino=...` | Frete direto por peça |
| `GET` | `/enderecos/cep/{cep}` | Auto-preenchimento via ViaCEP |

### Pedidos & Pagamento (RF05)
| Método | Rota | Descrição |
|--------|------|-----------|
| `POST` | `/pedidos/` | Cria pedido (valida estoque) |
| `GET` | `/pedidos/` | Histórico de pedidos |
| `POST` | `/pagamentos/` | Inicia pagamento (Cartão/Pix/Boleto) |
| `POST` | `/pagamentos/webhook` | Webhook do gateway |

---

## Configurações de Pool para NeonDB

O arquivo `app/database.py` detecta o `APP_ENV` e ajusta o pool automaticamente:

| APP_ENV | Pool | Indicado para |
|---------|------|---------------|
| `development` / `production` | `QueuePool` (5+5 conn) + recycle 270s | Docker, VPS, Render, Railway |
| `serverless` | `NullPool` (sem pool) | Vercel, AWS Lambda, Fly.io |

---

## Migrations (Alembic → Neon)

```bash
# Aplicar todas as migrations pendentes no Neon
alembic upgrade head

# Criar nova migration após alterar models
alembic revision --autogenerate -m "descricao da mudanca"

# Reverter última migration
alembic downgrade -1
```

---

## Variáveis de Ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DATABASE_URL` | ✅ | Connection string do NeonDB com `?sslmode=require` |
| `SECRET_KEY` | ✅ | Chave JWT — mín. 32 chars, gerada com `secrets.token_hex(32)` |
| `ALGORITHM` | — | Algoritmo JWT (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | — | Expiração do token (default: `60`) |
| `APP_ENV` | — | `development` \| `production` \| `serverless` |
| `CEP_API_URL` | — | URL do ViaCEP (default: `https://viacep.com.br/ws`) |
