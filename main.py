import uvicorn
from fastapi import FastAPI, Depends, Query
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, EmailStr
from bson import ObjectId
from datetime import datetime
from typing import Optional
from datetime import datetime

MONGO_DETAILS = "mongodb://localhost:27017"  

client = AsyncIOMotorClient(MONGO_DETAILS)
db = client.inventorydb  

item_collection = db.items  
clock_in_collection = db.clock_in_records  

app = FastAPI()

def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"],
        "item_name": item["item_name"],
        "quantity": item["quantity"],
        "expiry_date": item["expiry_date"],
        "insert_date": item["insert_date"]
    }

def clock_in_helper(clock_in) -> dict:
    return {
        "id": str(clock_in["_id"]),
        "email": clock_in["email"],
        "location": clock_in["location"],
        "insert_datetime": clock_in["insert_datetime"]
    }

class Item(BaseModel):
    name: str
    email: EmailStr
    item_name: str
    quantity: int
    expiry_date: str  

class ClockIn(BaseModel):
    email: EmailStr
    location: str

def convert_to_datetime(datetime_str: str):
    try:
        # Convert the string to a Python datetime object
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

def convert_to_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        return None  
    
    
@app.post("/items/")
async def create_item(item: Item):
    item_data = item.dict()

    expiry_datetime = convert_to_date(item_data['expiry_date'])
    if not expiry_datetime:
        return {"error": "Invalid expiry_date format. Use 'dd-mm-yyyy'."}
    item_data["expiry_date"] = expiry_datetime.strftime("%Y-%m-%d")


    item_data["insert_date"] = datetime.utcnow().strftime("%Y-%m-%d")

    result = await item_collection.insert_one(item_data)
    new_item = await item_collection.find_one({"_id": result.inserted_id})
    return item_helper(new_item)


@app.put("/items/{item_id}")
async def update_item(item_id: str, item: Item):
    item_data = item.dict()
    await item_collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_data})
    updated_item = await item_collection.find_one({"_id": ObjectId(item_id)})
    if updated_item:
        return item_helper(updated_item)
    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    delete_result = await item_collection.delete_one({"_id": ObjectId(item_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    return {"error": "Item not found"}

@app.get("/items/filter")
async def filter_items(
    email: Optional[EmailStr] = None,
    expiry_date: Optional[str] = None,
    insert_date: Optional[str] = None,
    quantity: Optional[int] = None
):
    query = {}
    if email:
        query["email"] = email
    if expiry_date:
        expiry_datetime = convert_to_date(expiry_date)
        if expiry_datetime:
            query["expiry_date"] = expiry_datetime.strftime("%Y-%m-%d")
        else:
            return {"error": "Invalid expiry_date format."}
    if insert_date:
        insert_datetime = convert_to_date(insert_date)
        if insert_datetime:
            query["insert_date"] = insert_datetime.strftime("%Y-%m-%d")
        else:
            return {"error": "Invalid insert_date format."}
    if quantity:
        query["quantity"] = {"$gte": quantity}

    items = await item_collection.find(query).to_list(100)
    return [item_helper(item) for item in items]


@app.get("/items/aggregate")
async def aggregate_items_by_email():
    pipeline = [
        {
            "$group": {
                "_id": "$email",  
                "item_count": {"$sum": 1}  
            }
        }
    ]
    aggregation_result = await item_collection.aggregate(pipeline).to_list(100)
    return [{"email": result["_id"], "item_count": result["item_count"]} for result in aggregation_result]

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    item = await item_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return item_helper(item)
    return {"error": "Item not found"}


@app.post("/clock-in/")
async def create_clock_in(clock_in: ClockIn):
    clock_in_data = clock_in.dict()
    clock_in_data["insert_datetime"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    result = await clock_in_collection.insert_one(clock_in_data)
    new_clock_in = await clock_in_collection.find_one({"_id": result.inserted_id})
    return clock_in_helper(new_clock_in)

@app.get("/clock-in/filter")
async def filter_clock_in(
    email: Optional[EmailStr] = None,
    location: Optional[str] = None,
    insert_datetime: Optional[str] = None
):
    query = {}
    
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        # Assuming insert_datetime is stored as a string in MongoDB
        insert_dt = convert_to_datetime(insert_datetime)
        print(insert_dt, "datetime123")
        if insert_dt:
            # If the datetime is valid, format it back to the original string format
            query["insert_datetime"] = insert_datetime  # This will match the string format exactly
        else:
            return {"error": "Invalid insert datetime format. Use 'YYYY-MM-DD HH:MM:SS' format."}
    
    clock_in_records = await clock_in_collection.find(query).to_list(10)
    
    return [clock_in_helper(clock_in) for clock_in in clock_in_records]

@app.get("/clock-in/{id}")
async def read_clock_in(id: str):
    clock_in = await clock_in_collection.find_one({"_id": ObjectId(id)})
    if clock_in:
        return clock_in_helper(clock_in)
    return {"error": "Clock-in record not found"}

@app.put("/clock-in/{id}")
async def update_clock_in(id: str, clock_in: ClockIn):
    clock_in_data = clock_in.dict()
    await clock_in_collection.update_one({"_id": ObjectId(id)}, {"$set": clock_in_data})
    updated_clock_in = await clock_in_collection.find_one({"_id": ObjectId(id)})
    if updated_clock_in:
        return clock_in_helper(updated_clock_in)
    return {"error": "Clock-in record not found"}

@app.delete("/clock-in/{id}")
async def delete_clock_in(id: str):
    delete_result = await clock_in_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Clock-in record deleted successfully"}
    return {"error": "Clock-in record not found"}


if __name__ == "__main__":
    uvicorn.run(app)
