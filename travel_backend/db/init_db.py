from travel_backend.db.db_setup import engine
from travel_backend.db.base import Base
from travel_backend.models import itinerary_models  # ensure all models are imported

def init_db():
    Base.metadata.create_all(bind=engine)
