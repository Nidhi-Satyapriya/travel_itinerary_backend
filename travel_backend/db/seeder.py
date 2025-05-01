from travel_backend.db.db_setup import SessionLocal
from travel_backend.db.init_db import init_db
from travel_backend.services.itinerary_logic import create_itinerary
from travel_backend.schemas.itinerary_schema import ItineraryCreate, DaySchema, ActivitySchema


def seed():
    # Step 1: Create the database tables
    init_db()

    # Step 2: Get a DB session
    db = SessionLocal()

    # Step 3: Define sample itinerary data
    sample_itinerary = ItineraryCreate(
        name="Phuket and Krabi Adventure",
        nights=4,
        days=[
            DaySchema(
                day_number=1,
                hotel="Phuket Beach Resort",
                transfer="Airport to hotel",
                activities=[
                    ActivitySchema(name="Arrival and Check-in", description="Check into the resort"),
                    ActivitySchema(name="Sunset Walk", description="Evening walk on the beach")
                ]
            ),
            DaySchema(
                day_number=2,
                hotel="Phuket Beach Resort",
                transfer=None,
                activities=[
                    ActivitySchema(name="Phi Phi Island Tour", description="Boat tour to the Phi Phi Islands"),
                    ActivitySchema(name="Snorkeling", description="Enjoy snorkeling in clear waters")
                ]
            ),
            DaySchema(
                day_number=3,
                hotel="Krabi Resort",
                transfer="Travel to Krabi by ferry",
                activities=[
                    ActivitySchema(name="Krabi Town Visit", description="Explore local market and food"),
                ]
            ),
            DaySchema(
                day_number=4,
                hotel="Krabi Resort",
                transfer=None,
                activities=[
                    ActivitySchema(name="Beach Day", description="Relax at Ao Nang Beach"),
                    ActivitySchema(name="Spa", description="Evening spa session at the resort")
                ]
            ),
        ]
    )

    # Step 4: Insert into DB
    try:
        create_itinerary(db, sample_itinerary)
        print("Sample itinerary seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding itinerary: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
