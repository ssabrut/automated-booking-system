import csv

from datetime import datetime

FILE_PATH = "data/booking.csv"

# with open("data/booking.csv", "r") as f:
#     reader = csv.reader(f)
#     next(reader)  # Skip header row
#     for row in reader:
#         name = row[1]
#         date = row[2]
#         start_time = datetime.datetime.strptime(row[3], "%H:%M").time()
#         end_time = datetime.datetime.strptime(row[4], "%H:%M").time()
#         if date == selected_date \
#             and selected_start_time <= start_time <= selected_end_time \
#                 and selected_start_time <= end_time <= selected_end_time:
#             print(name, date, start_time, end_time)