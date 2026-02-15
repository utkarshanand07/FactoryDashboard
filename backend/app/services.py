import random
import datetime
from sqlmodel import Session, select, func
from .models import Worker, Workstation, Event


def seed_data(session: Session):
    """Populates the DB with dummy data if empty."""
    if session.exec(select(Worker)).first():
        return

    print("Seeding dummy data...")

    # 1. Create Workers
    workers = [
        Worker(worker_id=f"W{i}", name=n)
        for i, n in enumerate(["Alice", "Bob", "Charlie", "Diana", "Evan", "Fiona"], 1)
    ]
    session.add_all(workers)

    # 2. Create Stations
    stations = [
        Workstation(workstation_id=f"S{i}", name=n)
        for i, n in enumerate(["Assembly", "Welding", "Painting", "Packaging", "QC", "Sorting"], 1)
    ]
    session.add_all(stations)
    session.commit()

    # 3. Create Dummy Events (Last 4 hours)
    now = datetime.datetime.utcnow()
    workers = session.exec(select(Worker)).all()
    stations = session.exec(select(Workstation)).all()

    for w in workers:
        current_time = now - datetime.timedelta(hours=4)
        while current_time < now:
            state = random.choices(["working", "idle", "product_count"], weights=[0.6, 0.3, 0.1])[0]
            count = random.randint(1, 5) if state == "product_count" else 0

            event = Event(
                timestamp=current_time,
                worker_id=w.worker_id,
                workstation_id=random.choice(stations).workstation_id,
                event_type=state,
                confidence=random.uniform(0.85, 0.99),
                count=count
            )
            session.add(event)
            current_time += datetime.timedelta(minutes=random.randint(5, 15))

    session.commit()
    print("Seeding complete.")


def calculate_utilization(working_count: int, total_count: int) -> float:
    if total_count == 0:
        return 0.0
    return round((working_count / total_count) * 100, 2)


def simulate_live_activity(session: Session):
    """
    Generates random events.
    """
    import datetime
    import random
    from .models import Worker, Workstation, Event

    workers = session.exec(select(Worker)).all()
    stations = session.exec(select(Workstation)).all()

    if not workers or not stations:
        return {"error": "No workers/stations found"}

    new_events = []
    now = datetime.datetime.utcnow()

    print(f"Simulating activity for {len(workers)} workers...")

    for w in workers:
        state = random.choices(["working", "idle", "product_count"], weights=[0.7, 0.2, 0.1])[0]
        count = random.randint(1, 3) if state == "product_count" else 0

        event = Event(
            timestamp=now,
            worker_id=w.worker_id,
            workstation_id=random.choice(stations).workstation_id,
            event_type=state,
            confidence=0.95,
            count=count
        )
        session.add(event)
        new_events.append(event)

    session.commit()
    return {"message": f"Added {len(new_events)} new events", "timestamp": str(now)}