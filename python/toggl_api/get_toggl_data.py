import csv

from toggl_api import TogglAPI

toggl = TogglAPI()
data = toggl.fetch_data(
    start_date="2024-03-12",
    end_date="2025-03-13",
)

for row in data:
    with open("toggl_data.csv", mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        writer.writeheader()
        writer.writerows(data)
