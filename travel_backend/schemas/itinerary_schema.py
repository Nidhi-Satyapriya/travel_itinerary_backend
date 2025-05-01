from typing import List, Optional
from pydantic import BaseModel, Field 

# Activity model for input (creation)
class ActivitySchema(BaseModel):
    name: str = Field(..., example="Island Hopping")
    description: Optional[str] = Field(None, example="Explore nearby islands by boat")


# Day model for input (creation)
class DaySchema(BaseModel):
    day_number: int = Field(..., gt=0, example=1)
    hotel: str = Field(..., example="Phuket Bay Resort")
    transfer: Optional[str] = Field(None, example="Ferry from Phuket to Krabi")
    activities: List[ActivitySchema] = Field(default_factory=list)


# Itinerary model for input (creation)
class ItineraryCreate(BaseModel):
    name: str = Field(..., example="Phuket and Krabi Escape")
    nights: int = Field(..., ge=1, le=30, example=5)
    days: List[DaySchema] = Field(..., min_items=1)

class HotelResponse(BaseModel):
    id: int
    name: str
    address: Optional[str] = None
    rating: Optional[int] = None

    model_config = {
        'from_attributes': True
    }


# Transfer model for response
class TransferResponse(BaseModel):
    id: int
    transfer_type: str
    from_location: str
    to_location: str

    model_config = {
        'from_attributes': True
    }

# Activity model for response
class ActivityResponse(ActivitySchema):
    id: int

    model_config = {
        'from_attributes': True
    }


# Day model for response
class DayResponse(BaseModel):
    id: int
    day_number: int
    hotel: str
    transfer: Optional[str]
    activities: List[ActivityResponse]

    model_config = {
        'from_attributes': True
    }


# Itinerary model for response
class ItineraryResponse(BaseModel):
    id: int
    name: str
    nights: int
    days: List[DayResponse] 

    model_config = {
        'from_attributes': True
    }