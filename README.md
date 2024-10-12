project setup
1. clone the repository
2. type 'pip install requirements.txt' on terminal 
3. uvicorn main:app  on terminal 
want to reload  then  'uvicorn main:app --reload' on terminal

Access this URL to view the running project: http://127.0.0.1:8000/docs#/


Key Features Implemented(Endpoints):

1. Items API:
POST /items: Creates a new item with an automatic insert_date.
GET /items/{item_id}: Retrieves an item by its ID.
GET /items/filter: Filters items by email, expiry date, insert date, or quantity.
PUT /items/{item_id}: Updates an item's details (excluding the insert_date).
DELETE /items/{item_id}: Deletes an item by ID.
Aggregation (GET /items/aggregate): Aggregates items based on email, showing the count of items per email.

2. Clock-In Records API:
POST /clock-in: Creates a new clock-in entry with an automatic insert_datetime.
GET /clock-in/{id}: Retrieves a clock-in record by ID.
GET /clock-in/filter: Filters clock-in records by email, location, or insert_datetime.
PUT /clock-in/{id}: Updates a clock-in record's details.
DELETE /clock-in/{id}: Deletes a clock-in record by ID.