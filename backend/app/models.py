import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import BaseModel

# --- Database Tables ---
class Worker(SQLModel, table=True):
    worker_id: str = Field(primary_key=True)
    name: str

class Workstation(SQLModel, table=True):
    workstation_id: str = Field(primary_key=True)
    name: str

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime.datetime
    worker_id: str = Field(index=True)
    workstation_id: str = Field(index=True)
    event_type: str  # 'working', 'idle', 'product_count'
    confidence: float
    count: int = 0

# --- Pydantic Models (for API validation) ---
class EventIngest(BaseModel):
    timestamp: datetime.datetime
    worker_id: str
    workstation_id: str
    event_type: str
    confidence: float
    count: int = 0