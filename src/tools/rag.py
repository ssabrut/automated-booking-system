import csv
from src.tools.properties import booking
from datetime import datetime
from langchain_core.tools import tool

FILE_PATH = "data/booking.csv"

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
def check_start_time(start_time: str) -> None:
    """
    Check the start time for the booking.
    """
    booking.start_time = datetime.strptime(start_time, "%H:%M").time()

@tool
def check_end_time(end_time: str) -> None:
    """
    Check the end time for the booking.
    """
    booking.end_time = datetime.strptime(end_time, "%H:%M").time()