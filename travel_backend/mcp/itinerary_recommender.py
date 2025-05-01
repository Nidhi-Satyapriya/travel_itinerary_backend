import logging
from typing import List
from collections import Counter

from sqlalchemy.orm import Session, joinedload
from travel_backend.models.itinerary_models import Itinerary, Day
from travel_backend.schemas.itinerary_schema import ItineraryResponse
from fastapi import HTTPException

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def recommend_itineraries_by_nights(db: Session, num_nights: int) -> List[ItineraryResponse]:
    """
    Fetch recommended itineraries based on the number of nights.
    Constraint: Nights must be between 2 and 8.
    Priority 1: Exact match on number of nights.
    Fallback: Most common number of days among all itineraries.
    """
    if num_nights < 2 or num_nights > 8:
        logger.warning(f"Invalid number of nights: {num_nights}. Must be between 2 and 8.")
        raise HTTPException(status_code=400, detail="Number of nights must be between 2 and 8.")

    try:
        logger.debug(f"Trying to fetch itineraries with {num_nights} nights...")

        # Primary query: exact nights match
        itineraries = (
            db.query(Itinerary)
            .options(joinedload(Itinerary.days).joinedload(Day.activities))
            .filter(Itinerary.nights == num_nights)
            .all()
        )

        logger.debug(f"Found {len(itineraries)} itineraries with {num_nights} nights.")  # Check how many itineraries found

        if itineraries:
            return [ItineraryResponse.from_orm(itinerary) for itinerary in itineraries]

        logger.debug(f"No exact matches for {num_nights} nights. Falling back to most common day count.")

        # Fallback: All itineraries
        all_itineraries = (
            db.query(Itinerary)
            .options(joinedload(Itinerary.days).joinedload(Day.activities))
            .all()
        )

        if not all_itineraries:
            logger.warning("No itineraries found at all in the database.")
            return []

        # Count how many days each itinerary has
        day_counts = [len(itinerary.days) for itinerary in all_itineraries if itinerary.days]
        logger.debug(f"Day counts: {day_counts}")  # Log the day counts

        if not day_counts:
            logger.warning("Itineraries exist, but none have valid days.")
            return []

        # Get most common number of days
        recommended_days = Counter(day_counts).most_common(1)[0][0]
        logger.debug(f"Most common day count: {recommended_days}")

        # Filter itineraries that match the common day count
        recommended = [
            ItineraryResponse.from_orm(itinerary)
            for itinerary in all_itineraries
            if len(itinerary.days) == recommended_days
        ]

        logger.debug(f"Returning {len(recommended)} itineraries with {recommended_days} days.")
        return recommended

    except Exception as e:
        logger.exception("Error while recommending itineraries")
        return []
