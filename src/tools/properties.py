from langchain_core.pydantic_v1 import BaseModel

class Booking(BaseModel):
    """
    A model representing a booking.

    Attributes:
        id (str): The unique identifier for the booking.
        name (str): The name associated with the booking.
        date (str): The date of the booking.
        start_time (str): The start time of the booking.
        end_time (str): The end time of the booking.
    """
    
    id: str
    name: str
    date: str
    start_time: str
    end_time: str