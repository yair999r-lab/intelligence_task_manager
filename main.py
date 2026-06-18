from routes import agent_rotes
from database.db_connection import DB_connection

from fastapi import FastAPI
from contextlib import asynccontextmanager

async def lifespan(app:FastAPI):

    db = DB_connection()
    conn = db.get_connection()
    db.create_database()
    db.create_tabels()
    




app = FastAPI(lifespan=lifespan)