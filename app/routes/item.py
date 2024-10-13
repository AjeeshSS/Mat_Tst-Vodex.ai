from fastapi import APIRouter, Depends
from app.models.item import Item
from app.core.database import item_collection
from app.utils.item_helper import item_helper, convert_to_date
from datetime import datetime
from bson import ObjectId
from typing import Optional


router = APIRouter()

@router.post("/items/")
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

@router.put("/{item_id}")
async def update_item(item_id: str, item: Item):
    item_data = item.dict()
    await item_collection.update_one({"_id": ObjectId(item_id)}, {"$set": item_data})
    updated_item = await item_collection.find_one({"_id": ObjectId(item_id)})
    if updated_item:
        return item_helper(updated_item)
    return {"error": "Item not found"}

@router.delete("/{item_id}")
async def delete_item(item_id: str):
    delete_result = await item_collection.delete_one({"_id": ObjectId(item_id)})
    if delete_result.deleted_count == 1:
        return {"message": "Item deleted successfully"}
    return {"error": "Item not found"}

@router.get("/items/filter")
async def filter_items(
    email: Optional[str] = None,
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
        query["quantity"] = quantity
    items = await item_collection.find(query).to_list(100)
    return [item_helper(item) for item in items]


@router.get("/aggregate")
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


@router.get("/{item_id}")
async def read_item(item_id: str):
    item = await item_collection.find_one({"_id": ObjectId(item_id)})
    if item:
        return item_helper(item)
    return {"error": "Item not found"}