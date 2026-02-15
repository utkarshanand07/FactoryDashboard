from sqlmodel import SQLModel, create_engine, Session

# Use a file-based DB for persistence, or ":memory:" for testing
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def get_session():
    """Dependency to provide a DB session to endpoints."""
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    """Creates tables if they don't exist."""
    SQLModel.metadata.create_all(engine)