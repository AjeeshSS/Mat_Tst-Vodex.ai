from datetime import datetime

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

def convert_to_date(date_str: str):
    try:
        return datetime.strptime(date_str, "%d-%m-%Y")
    except ValueError:
        return None
