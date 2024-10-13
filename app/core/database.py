from motor.motor_asyncio import AsyncIOMotorClient

MONGO_DETAILS = "mongodb://localhost:27017"

client = AsyncIOMotorClient(MONGO_DETAILS)

db = client.inventorydb

item_collection = db.items
clock_in_collection = db.clock_in_records
