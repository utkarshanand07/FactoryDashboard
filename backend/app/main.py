from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from .database import create_db_and_tables, engine
from .services import seed_data
from .routers import ingest, metrics

app = FastAPI(title="FactoryAI Dashboard")

# --- CORS (Allow Frontend to talk to Backend) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Register Routers ---
app.include_router(ingest.router)
app.include_router(metrics.router)

# --- Startup Event ---
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        seed_data(session)

@app.get("/")
def health_check():
    return {"status": "ok", "version": "2.0.0 (Modular)"}