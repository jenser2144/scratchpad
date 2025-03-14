# Toggl API

## Setup
Create python virtual environment
```bash
python3 -m venv venv
```
Install python dependencies:
```bash
pip install -r requirements.txt
```
Create _.env_ file in this directory with Toggl account information. Should look like the following:
```
TOGGL_USERNAME=<toggl_username>
TOGGL_PASSWORD=<toggl_password>
TOGGL_WORKSPACE_ID=<toggl_workspace_id>
```