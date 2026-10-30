import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text

from app.routers import calculator, history

app = FastAPI(title="Mini Calculator API")

database_url = os.getenv(
    "DATABASE_URL",
    "mysql+mysqlconnector://appuser:classroom-app@localhost:3306/appdb",
)
engine = create_engine(database_url, pool_pre_ping=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(calculator.router)
app.include_router(history.router)


@app.get("/test-db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar_one()
    return {"db_result": result}
