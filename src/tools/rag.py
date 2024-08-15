import csv

from datetime import datetime
from typing import Iterator
from langchain_core.document_loaders import BaseLoader
from langchain_core.documents import Document

class DocumentLoader(BaseLoader):
    """
    A document loader that reads booking data from a CSV file and yields Document objects.

    Attributes:
        file_path (str): The path to the CSV file containing booking data.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the DocumentLoader with the path to the CSV file.

        Args:
            file_path (str): The path to the CSV file containing booking data.
        """
        self.file_path = file_path

    def lazy_load(self) -> Iterator[Document]:
        """
        Lazily loads booking data from the CSV file and yields Document objects.

        Yields:
            Iterator[Document]: An iterator of Document objects, each representing a row in the CSV file.
        """
        with open(self.file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)  # Skip header row
            for row in reader:
                _id = row[0]
                name = row[1]
                date = row[2]
                start_time = datetime.strptime(row[3], "%H:%M").time()
                end_time = datetime.strptime(row[4], "%H:%M").time()
                yield Document(
                    page_content=_id,
                    metadata={
                        "name": name,
                        "date": date,
                        "start_time": start_time,
                        "end_time": end_time
                    }
                )