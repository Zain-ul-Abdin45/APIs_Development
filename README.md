
# async-fastapi-demo

Production-grade reference for **async FastAPI** wired to MongoDB (Motor), PostgreSQL (SQLAlchemy async + asyncpg), and an external HTTP API (httpx) — all running concurrently inside a single event loop thread.

Companion code for the Substack article: *`async def` Is a Promise. Your Database Driver Is Breaking It.*

---

## What this demonstrates

| Problem | Fix shown here |
|---|---|
| `pymongo` blocks the event loop | `motor` async driver |
| SQLAlchemy sync session blocks the event loop | `AsyncSession` + `asyncpg` |
| `requests` blocks the event loop | `httpx.AsyncClient` |
| Sequential `await` on independent queries | `asyncio.gather()` |
| CPU-bound work blocking async routes | `run_in_executor` pattern |

---

## Project layout

```
app/
├── config.py              # Pydantic Settings — reads .env
├── main.py                # FastAPI app, lifespan, CORS
│
├── db/
│   ├── mongo.py           # Motor client singleton
│   └── postgres.py        # async engine + session factory
│
├── models/
│   ├── account.py         # Pydantic response models
│   └── transaction.py     # SQLAlchemy ORM + Pydantic schema
│
├── repositories/
│   ├── account_repo.py    # MongoDB read/write via Motor
│   └── transaction_repo.py # PostgreSQL read via asyncpg
│
├── services/
│   ├── account_service.py # asyncio.gather — all three in parallel
│   └── exchange_service.py # httpx AsyncClient, reused across requests
│
└── routes/
    └── account.py         # GET /accounts/{id}/summary
```

---

## Local setup

### 1. Clone and install

```bash
git clone https://github.com/your-handle/async-fastapi-demo
cd async-fastapi-demo
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# edit .env — set your DB URIs and API keys
```

### 3. Start the databases (Docker)

```bash
# MongoDB
docker run -d --name mongo -p 27017:27017 mongo:7

# PostgreSQL
docker run -d --name postgres \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=financedb \
  -p 5432:5432 postgres:16
```

### 4. Run

```bash
uvicorn app.main:app --reload
```

Swagger UI at `http://localhost:8000/docs`

---

## Production hardening

### SSH tunnels for managed databases

Never expose database ports directly. Tunnel through a bastion:

```bash
# MongoDB Atlas or self-hosted behind bastion
ssh -N -L 27017:mongo-host.internal:27017 bastion-user@bastion.example.com

# PostgreSQL (RDS / Cloud SQL)
ssh -N -L 5432:pg-host.internal:5432 bastion-user@bastion.example.com
```

Then use `localhost` URIs in `.env`:
```
MONGO_URI=mongodb://localhost:27017
POSTGRES_URI=postgresql+asyncpg://user:password@localhost:5432/financedb
```

### TLS for MongoDB

```
MONGO_URI=mongodb+srv://user:password@cluster.mongodb.net/accounts?tls=true&tlsCAFile=/etc/ssl/certs/ca-certificates.crt
```

### SSL for PostgreSQL (asyncpg)

```python
# in app/db/postgres.py — add to create_async_engine:
import ssl
ssl_ctx = ssl.create_default_context(cafile="/path/to/ca.pem")

engine = create_async_engine(
    settings.postgres_uri,
    connect_args={"ssl": ssl_ctx},
    ...
)
```

### Secret management

In production, pull secrets from a secrets manager instead of `.env`:

```python
# AWS Secrets Manager example
import boto3, json

def load_secret(secret_name: str) -> dict:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response["SecretString"])
```

---

## Architecture

See [architecture.md](architecture.md) for Mermaid diagrams covering:
- Full request flow
- Event loop concurrency model
- Module dependency graph
- Broken vs fixed corridor analogy
- Connection lifecycle state machine

---

## Key files to read first

1. [app/services/account_service.py](app/services/account_service.py) — `asyncio.gather` wiring all three I/O sources
2. [app/db/postgres.py](app/db/postgres.py) — async engine + session factory
3. [app/db/mongo.py](app/db/mongo.py) — Motor client singleton
4. [app/services/exchange_service.py](app/services/exchange_service.py) — shared httpx client

---

## Running tests

```bash
pip install pytest pytest-asyncio httpx
pytest tests/ -v
```

---

## License

MIT
=======
# APIs_Development
c1b2ad775bbb53dd4a0ec459de595a997dfe0e3b
