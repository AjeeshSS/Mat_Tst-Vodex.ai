from fastapi import APIRouter
from app.models.clock_in import ClockIn
from app.core.database import clock_in_collection
from app.utils.clock_in_helper import clock_in_helper, convert_to_datetime
from datetime import datetime
from bson import ObjectId
from typing import Optional


router = APIRouter()

@router.post("/clock-in/")
async def create_clock_in(clock_in: ClockIn):
    clock_in_data = clock_in.dict()
    clock_in_data["insert_datetime"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    result = await clock_in_collection.insert_one(clock_in_data)
    new_clock_in = await clock_in_collection.find_one({"_id": result.inserted_id})
    return clock_in_helper(new_clock_in)

@router.put("/{id}")
async def update_clock_in(id: str, clock_in: ClockIn):
    clock_in_data = clock_in.dict()
    await clock_in_collection.update_one({"_id": ObjectId(id)}, {"$set": clock_in_data})
    updated_clock_in = await clock_in_collection.find_one({"_id": ObjectId(id)})
    if updated_clock_in:
        return clock_in_helper(updated_clock_in)
    return {"error": "Clock-in record not found"}

@router.delete("/{id}")
async def delete_clock_in(id: str):
    delete_result = await clock_in_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return {"message": "Clock-in record deleted successfully"}
    return {"error": "Clock-in record not found"}

@router.get("/clock-in/filter")
async def filter_clock_in(
    email: Optional[str] = None,
    location: Optional[str] = None,
    insert_datetime: Optional[str] = None
):
    query = {}
    if email:
        query["email"] = email
    if location:
        query["location"] = location
    if insert_datetime:
        insert_dt = convert_to_datetime(insert_datetime)
        if insert_dt:
            query["insert_datetime"] = insert_datetime
        else:
            return {"error": "Invalid insert_datetime format. Use 'YYYY-MM-DD HH:MM:SS'."}
    clock_in_records = await clock_in_collection.find(query).to_list(10)
    return [clock_in_helper(clock_in) for clock_in in clock_in_records]

@router.get("/{id}")
async def read_clock_in(id: str):
    clock_in = await clock_in_collection.find_one({"_id": ObjectId(id)})
    if clock_in:
        return clock_in_helper(clock_in)
    return {"error": "Clock-in record not found"}
