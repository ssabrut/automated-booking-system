from typing import Any

class Booking:
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

    def __getattribute__(self, name: str) -> Any:
        """
        Retrieve an attribute of the booking.

        Args:
            name (str): The name of the attribute to retrieve.

        Returns:
            Any: The value of the requested attribute.
        """
        return super().__getattribute__(name)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Set an attribute of the booking.

        Args:
            name (str): The name of the attribute to set.
            value (Any): The value to set for the attribute.
        """
        super().__setattr__(name, value)