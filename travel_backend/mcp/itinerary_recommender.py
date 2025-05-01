import logging
from typing import List
from collections import Counter

from sqlalchemy.orm import Session, joinedload
from travel_backend.models.itinerary_models import Itinerary
from travel_backend.schemas.itinerary_schema import ItineraryResponse

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def recommend_itineraries_by_nights(db: Session, num_nights: int) -> List[ItineraryResponse]:
    """
    Fetch recommended itineraries based on the number of nights.
    Priority 1: Exact match on number of nights.
    Fallback: Most common number of days among all itineraries.
    """
    try:
        logger.debug(f"Trying to fetch itineraries with {num_nights} nights...")

        # Primary query: exact nights match
        itineraries = (
            db.query(Itinerary)
            .options(joinedload(Itinerary.days).joinedload("activities"))
            .filter(Itinerary.nights == nights)
            .all()
        )

        if itineraries:
            logger.debug(f"Found {len(itineraries)} itineraries with {num_nights} nights.")
            return [ItineraryResponse.from_orm(itinerary) for itinerary in itineraries]

        logger.debug(f"No exact matches for {num_nights} nights. Falling back to most common day count.")

        # Fallback: All itineraries
        all_itineraries = (
            db.query(Itinerary)
            .options(joinedload(Itinerary.days).joinedload("activities"))
            .all()
        )

        if not all_itineraries:
            logger.warning("No itineraries found at all in the database.")
            return []

        # Count how many days each itinerary has
        day_counts = [len(itinerary.days) for itinerary in all_itineraries if itinerary.days]
        if not day_counts:
            logger.warning("Itineraries exist, but none have days.")
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
