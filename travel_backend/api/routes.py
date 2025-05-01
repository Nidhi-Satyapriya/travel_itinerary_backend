from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from travel_backend.db.db_setup import SessionLocal
from travel_backend.services.itinerary_logic import create_itinerary, get_all_itineraries, get_itinerary_by_id
from travel_backend.mcp.itinerary_recommender import recommend_itineraries_by_nights
from travel_backend.schemas.itinerary_schema import ItineraryCreate, ItineraryResponse
from travel_backend.models.itinerary_models import Itinerary

# Define the router
router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST: Create an itinerary
@router.post("/itineraries/", response_model=ItineraryResponse)
def create_itinerary_route(itinerary: ItineraryCreate, db: Session = Depends(get_db)):
    try:
        # Call the function to create the itinerary
        db_itinerary = create_itinerary(db, itinerary)
        return db_itinerary
    except SQLAlchemyError as e:
        # Handle database errors and provide a clear error message
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(status_code=500, detail=f"Error creating itinerary: {str(e)}")

# GET: List all itineraries
@router.get("/itineraries/", response_model=List[ItineraryResponse])
def list_itineraries(db: Session = Depends(get_db)):
    try:
        itineraries = get_all_itineraries(db)
        if not itineraries:
            raise HTTPException(status_code=404, detail="No itineraries found")
        return itineraries
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving itineraries: {str(e)}")

# GET: Get a specific itinerary by ID
@router.get("/itineraries/{itinerary_id}", response_model=ItineraryResponse)
def get_itinerary(itinerary_id: int, db: Session = Depends(get_db)):
    try:
        itinerary = get_itinerary_by_id(db, itinerary_id)
        if itinerary is None:
            raise HTTPException(status_code=404, detail="Itinerary not found")
        return itinerary
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving itinerary: {str(e)}")
    
# GET: Get recommended itineraries
@router.get("/recommendations/{nights}", response_model=List[ItineraryResponse])
def get_recommendations(nights: int, db: Session = Depends(get_db)):
    return recommend_itineraries_by_nights(db, nights)