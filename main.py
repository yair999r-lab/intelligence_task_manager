from routes.agent_rotes import route as agents_route
from routes.mission_routes import route as mission_route
from routes.report_routes import route as repo_route
from database.db_connection import db

from fastapi import FastAPI
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app:FastAPI):

    
    conn = db.get_connection()
    db.create_database()
    db.create_tabels()

    yield
    
    conn.close()

app = FastAPI(lifespan=lifespan)

app.include_router(agents_route)
app.include_router(mission_route)
app.include_router(repo_route)