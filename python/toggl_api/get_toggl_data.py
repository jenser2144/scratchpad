import csv

from toggl_api import TogglAPI

toggl = TogglAPI()

# Fetch organization metadata
organization_data = toggl.get_organization()

# Fetch workspace id's
workspace_ids = toggl.get_workspace_ids()

# For each workspace, get workspace metadata and time entries
all_workspace_data = []
all_time_entry_data = []
for workspace_id in workspace_ids:
    workspace_data = toggl.get_workspace(workspace_id=workspace_id)
    all_workspace_data += [workspace_data]

    projects_data = toggl.get_projects(workspace_id=workspace_id)

    time_entry_data = toggl.fetch_data(
        workspace_id=workspace_id,
        start_date="2024-01-01",
        end_date="2025-11-01",
    )
    all_time_entry_data += time_entry_data

# Write all data to csv files
with open("toggl_organizations.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=organization_data.keys())
    writer.writeheader()
    writer.writerows([organization_data])

with open("toggl_projects.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=projects_data[0].keys())
    writer.writeheader()
    writer.writerows(projects_data)

with open("toggl_workspaces.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=all_workspace_data[0].keys())
    writer.writeheader()
    writer.writerows(all_workspace_data)

with open("toggl_data.csv", mode="w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=all_time_entry_data[0].keys())
    writer.writeheader()
    writer.writerows(all_time_entry_data)
