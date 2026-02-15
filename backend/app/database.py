import os
from sqlmodel import SQLModel, create_engine, Session

# 1. Get DB URL from Environment Variable, or use default local file
# On Render, this might be an internal Postgres URL if you upgrade later.
# For now, we use a file path that works in Docker.
sqlite_file_name = os.getenv("DATABASE_URL", "database.db")

# Handle the case where the URL might be for Postgres (Render) vs SQLite
if sqlite_file_name.startswith("postgres"):
    database_url = sqlite_file_name
    connect_args = {} # Postgres doesn't need check_same_thread
else:
    # Ensure it starts with sqlite:/// if it's just a filename
    if not sqlite_file_name.startswith("sqlite"):
        database_url = f"sqlite:///{sqlite_file_name}"
    else:
        database_url = sqlite_file_name
    connect_args = {"check_same_thread": False}

# 2. Create Engine
engine = create_engine(database_url, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)