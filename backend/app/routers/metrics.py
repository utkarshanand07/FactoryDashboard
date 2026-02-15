from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from ..database import get_session
from ..models import Event, Worker, Workstation
from ..services import calculate_utilization

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])


@router.get("/factory")
def get_factory_metrics(session: Session = Depends(get_session)):
    total_products = session.exec(select(func.sum(Event.count))).one() or 0

    total_events = session.exec(select(func.count(Event.id)).where(Event.event_type != 'product_count')).one()
    working_events = session.exec(select(func.count(Event.id)).where(Event.event_type == 'working')).one()

    utilization = calculate_utilization(working_events, total_events)

    return {
        "total_production": total_products,
        "global_utilization": utilization,
        "active_cameras": 6
    }


@router.get("/workers")
def get_worker_metrics(session: Session = Depends(get_session)):
    workers = session.exec(select(Worker)).all()
    results = []
    for w in workers:
        products = session.exec(select(func.sum(Event.count)).where(Event.worker_id == w.worker_id)).one() or 0
        w_events = session.exec(
            select(func.count(Event.id)).where(Event.worker_id == w.worker_id, Event.event_type == 'working')).one()
        total_ev = session.exec(select(func.count(Event.id)).where(Event.worker_id == w.worker_id,
                                                                   Event.event_type != 'product_count')).one()

        results.append({
            "id": w.worker_id,
            "name": w.name,
            "produced": products,
            "utilization": calculate_utilization(w_events, total_ev),
            "status": "Active" if total_ev > 0 else "Inactive"
        })
    return results