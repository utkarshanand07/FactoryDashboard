from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..database import get_session
from ..models import EventIngest, Event
from ..services import simulate_live_activity

router = APIRouter(prefix="/api/ingest", tags=["Ingestion"])

@router.post("")
def ingest_event(event_data: EventIngest, session: Session = Depends(get_session)):
    try:
        db_event = Event(**event_data.dict())
        session.add(db_event)
        session.commit()
        return {"status": "success", "id": db_event.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulate")
def trigger_simulation(session: Session = Depends(get_session)):
    """Triggers the backend to generate fake data immediately."""
    result = simulate_live_activity(session)
    return result