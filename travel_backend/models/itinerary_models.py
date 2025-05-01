from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from travel_backend.db.base import Base  

# Represents a full travel itinerary 
class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)  #constraints
    name = Column(String, nullable=False)              
    nights = Column(Integer, nullable=False)           

    # One-to-many relationship: one itinerary has many days
    days = relationship(
        "Day",
        back_populates="itinerary",
        cascade="all, delete-orphan"  
    )


# Represents a single day in an itinerary
class Day(Base):
    __tablename__ = "days"

    id = Column(Integer, primary_key=True, index=True) #constraints
    day_number = Column(Integer, nullable=False)      
    hotel = Column(String, nullable=False)             
    transfer = Column(String)                           

    # Foreign key to Itinerary
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"), nullable=False)  # Required FK
    itinerary = relationship("Itinerary", back_populates="days")  # Many-to-one

    # One-to-many relationship: one day has many activities
    activities = relationship(
        "Activity",
        back_populates="day",
        cascade="all, delete-orphan"  # Deletes activities if day is deleted
    )


# Represents an activity on a specific day
class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)  #constraints
    name = Column(String, nullable=False)              
    description = Column(String)                       

    # Foreign key to Day
    day_id = Column(Integer, ForeignKey("days.id"), nullable=False)  # Required FK
    day = relationship("Day", back_populates="activities")  # Many-to-one
