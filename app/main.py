from fastapi import FastAPI
from app.routes import item, clock_in

app = FastAPI()

app.include_router(item.router, prefix="/items", tags=["Items"])
app.include_router(clock_in.router, prefix="/clock-in", tags=["Clock In"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
