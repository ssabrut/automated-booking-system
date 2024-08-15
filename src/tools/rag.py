import csv
from src.tools.properties import booking
from datetime import datetime
from langchain_core.tools import tool

FILE_PATH = "data/booking.csv"

@tool
def set_name(name: str) -> str:
    """
    Set the name for the booking.

    Args:
        name (str): The name to set for the booking.

    Returns:
        str: The name that was set.
    """
    booking.name = name

@tool
def set_date(date: str) -> str:
    """
    Set the date for the booking.

    Args:
        date (str): The date to set for the booking.

    Returns:
        str: The date that was set.
    """
    booking.date = date

@tool
def set_start_time(start_time: str) -> str:
    """
    Set the start time for the booking.

    Args:
        start_time (str): The start time to set for the booking in "HH:MM" format.

    Returns:
        str: The start time that was set.
    """
    booking.start_time = datetime.strptime(start_time, "%H:%M").time()

@tool
def set_end_time(end_time: str) -> str:
    """
    Set the end time for the booking.

    Args:
        end_time (str): The end time to set for the booking in "HH:MM" format.

    Returns:
        str: The end time that was set.
    """
    booking.end_time = datetime.strptime(end_time, "%H:%M").time()