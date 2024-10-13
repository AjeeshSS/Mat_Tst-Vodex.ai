from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import MONGO_DETAILS


client = AsyncIOMotorClient(MONGO_DETAILS)

db = client.inventorydb

item_collection = db.items
clock_in_collection = db.clock_in_records
