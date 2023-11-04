from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.client_session import ClientSession
from app.config import settings


def get_client(mongodb_url: str) -> AsyncIOMotorClient:
    """Get mongo db

    Args:
        mongodb_url (str): url to mongo

    Returns:
        AsyncIOMotorClient: client exemplar
    """
    return AsyncIOMotorClient(mongodb_url)


client = get_client(settings.MONGODB_URL.get_secret_value())
