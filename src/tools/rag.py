from src.tools.properties import booking
from datetime import datetime
from langchain_core.tools import tool

@tool
def check_name(name: str) -> None:
    """
    Check the name for the booking.
    """
    booking.name = name

@tool
def check_date(date: str) -> None:
    """
    Check the date for the booking.
    """
    booking.date = date

@tool
def check_time_range(start_time: str, end_time: str) -> None:
    """
    Check the time range for the booking.
    """
    booking.start_time = datetime.strptime(start_time, "%H:%M").time()
    booking.end_time = datetime.strptime(end_time, "%H:%M").time()