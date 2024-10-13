from datetime import datetime

def clock_in_helper(clock_in) -> dict:
    return {
        "id": str(clock_in["_id"]),
        "email": clock_in["email"],
        "location": clock_in["location"],
        "insert_datetime": clock_in["insert_datetime"]
    }

def convert_to_datetime(datetime_str: str):
    try:
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None
