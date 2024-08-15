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

@tool
def check_time_range(start_time: str, end_time: str) -> None:
    """
    Check the time range for the booking.
    """
    booking.start_time = datetime.strptime(start_time, "%H:%M").time()
    booking.end_time = datetime.strptime(end_time, "%H:%M").time()

@tool
def check_available_time() -> None:
    """
    Check the available time for the booking.
    """
    print("a")
    with open(FILE_PATH, "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            date = row[2]
            start_time = datetime.strptime(row[3], "%H:%M").time()
            end_time = datetime.strptime(row[4], "%H:%M").time()
            if date == booking.date \
                and booking.start_time <= start_time <= booking.end_time \
                    and booking.start_time <= end_time <= booking.end_time:
                print(row[1], date, start_time, end_time)