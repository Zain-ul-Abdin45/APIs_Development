# Architecture

## Request Flow

```mermaid
flowchart TD
    Client([HTTP Client]) -->|GET /accounts/:id/summary| Route

    subgraph FastAPI["FastAPI — single event loop thread"]
        Route["routes/account.py\nasync def account_summary()"]
        Service["services/account_service.py\nawait asyncio.gather(...)"]
        Route --> Service
    end

    subgraph Repos["Repositories — yield at every await"]
        AR["repositories/account_repo.py\nfind_account()"]
        TR["repositories/transaction_repo.py\nget_transactions()"]
    end

    subgraph External["External I/O — all non-blocking"]
        Mongo[("MongoDB\nvia Motor")]
        Postgres[("PostgreSQL\nvia asyncpg")]
        ExAPI["Exchange Rate API\nvia httpx"]
    end

    Service -->|"await — yields to loop"| AR
    Service -->|"await — yields to loop"| TR
    Service -->|"await — yields to loop"| ES["services/exchange_service.py\nget_exchange_rate()"]

    AR -->|"async find_one()"| Mongo
    TR -->|"async session.execute()"| Postgres
    ES -->|"async client.get()"| ExAPI
```

## Module Layout

```mermaid
flowchart LR
    config["app/config.py\nPydantic Settings\nreads .env"]

    subgraph DB["app/db/"]
        mongo["mongo.py\nMotor client\nsingleton"]
        postgres["postgres.py\nasync engine\n+ session factory"]
    end

    subgraph Models["app/models/"]
        am["account.py\nAccount\nAccountSummary"]
        tm["transaction.py\nTransactionORM\nTransaction"]
    end

    subgraph Repos["app/repositories/"]
        ar["account_repo.py\nfind_account()\nupsert_account()"]
        tr["transaction_repo.py\nget_transactions()"]
    end

    subgraph Services["app/services/"]
        es["exchange_service.py\nget_exchange_rate()\nhttpx AsyncClient"]
        as_["account_service.py\nget_account_summary()\nasyncio.gather()"]
    end

    subgraph Routes["app/routes/"]
        route["account.py\nGET /accounts/:id/summary"]
    end

    config --> DB
    DB --> Repos
    Models --> Repos
    Models --> Services
    Repos --> Services
    Services --> Routes
```

## Concurrency Model: What the Event Loop Sees

```mermaid
sequenceDiagram
    participant Loop as Event Loop
    participant Req as Request Handler
    participant Mongo as Motor (MongoDB)
    participant PG as asyncpg (PostgreSQL)
    participant HTTP as httpx (Exchange API)

    Req->>Loop: asyncio.gather(mongo, pg, http)
    Loop->>Mongo: find_one() — send query, yield
    Loop->>PG: execute() — send query, yield
    Loop->>HTTP: GET /live — send request, yield

    Note over Loop: Loop is FREE while all 3 are in flight.<br/>Other incoming requests run here.

    Mongo-->>Loop: result ready
    PG-->>Loop: result ready
    HTTP-->>Loop: result ready

    Loop-->>Req: all 3 resolved → assemble response
```

## Broken vs Fixed: The Corridor Analogy

```mermaid
flowchart TD
    subgraph Broken["Broken — sync driver inside async route"]
        B_Door["async def route()\n[door is open]"]
        B_Call["pymongo.find_one()\n[holds the thread]"]
        B_Queue["Request 2, 3, 4...\n[frozen in corridor]"]
        B_Door --> B_Call --> B_Queue
    end

    subgraph Fixed["Fixed — async driver + asyncio.gather"]
        F_Door["async def route()\n[door is open]"]
        F_Call["await motor.find_one()\n[yields — loop is free]"]
        F_Other["Other requests run\nwhile I/O is in flight"]
        F_Door --> F_Call
        F_Call -.->|"event loop switches"| F_Other
    end
```

## Connection Lifecycle

```mermaid
stateDiagram-v2
    [*] --> Uninitialized: app starts

    Uninitialized --> Connected: first request triggers\nlazy initialisation

    Connected --> InUse: request borrows\nfrom pool

    InUse --> Connected: await completes,\nconnection returned

    Connected --> Closed: app shutdown\n(lifespan context exits)

    Closed --> [*]
```
