from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.config import settings

_client: AsyncIOMotorClient | None = None


def get_mongo_client() -> AsyncIOMotorClient:
    global _client
    if _client is None:
        _client = AsyncIOMotorClient(
            settings.mongo_uri,
            serverSelectionTimeoutMS=5000,
            # TLS/SSL — enable in prod by setting MONGO_URI with tls=true
            # and pointing to CA cert: tlsCAFile=/path/to/ca.pem
        )
    return _client


def get_mongo_db() -> AsyncIOMotorDatabase:
    return get_mongo_client()[settings.mongo_db]


async def close_mongo():
    global _client
    if _client is not None:
        _client.close()
        _client = None
