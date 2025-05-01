from sqlalchemy.orm import Session
from travel_backend.models.itinerary_models import Itinerary, Day, Activity
from travel_backend.schemas.itinerary_schema import ItineraryCreate

# Create Itinerary
def create_itinerary(db: Session, itinerary: ItineraryCreate):
    db_itinerary = Itinerary(
        name=itinerary.name,
        nights=itinerary.nights
    )
    
    # Insert days and activities
    for day in itinerary.days:
        db_day = Day(
            day_number=day.day_number,
            hotel=day.hotel,
            transfer=day.transfer,
            itinerary=db_itinerary
        )
        db.add(db_day)
        
        for activity in day.activities:
            db_activity = Activity(
                name=activity.name,
                description=activity.description,
                day=db_day
            )
            db.add(db_activity)

    db.commit()
    db.refresh(db_itinerary)  # Ensure the inserted data is up to date
    return db_itinerary

# Get All Itineraries
def get_all_itineraries(db: Session):
    return db.query(Itinerary).all()

# Get Itinerary by ID
def get_itinerary_by_id(db: Session, itinerary_id: int):
    return db.query(Itinerary).filter(Itinerary.id == itinerary_id).first()
