import csv

from toggl_api import TogglAPI

toggl = TogglAPI()
workspace_ids = toggl.get_workspace_ids()

all_data = []
for workspace_id in workspace_ids:
    data = toggl.fetch_data(
        workspace_id=workspace_id,
        start_date="2024-01-01",
        end_date="2025-11-01",
    )
    all_data.append(data)

for d in all_data:
    for row in data:
        with open("toggl_data.csv", mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=row.keys())
            writer.writeheader()
            writer.writerows(data)
