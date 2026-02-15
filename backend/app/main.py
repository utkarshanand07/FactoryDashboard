import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # <--- IMPORT THIS
from sqlmodel import Session

from .database import create_db_and_tables, engine
from .services import seed_data
from .routers import ingest, metrics

app = FastAPI(title="FactoryAI Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router)
app.include_router(metrics.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        seed_data(session)

if os.getenv("DOCKER_ENV"):
    frontend_path = "/app/frontend"
else:
    frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")