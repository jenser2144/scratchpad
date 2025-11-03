from base64 import b64encode
from calendar import monthrange
from datetime import datetime, timedelta
# import json
import logging
from os import getenv
import re

from dotenv import load_dotenv
import requests

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class TogglAPI:
    """Class to interact with the Toggl Api"""

    def __init__(self):
        """Initialize the TogglAPI class"""
        self.email, self.password, self.organization_id = self._get_env_variables()
        self.base_url = "https://api.track.toggl.com"
        self.headers = self._create_headers()

    def _get_env_variables(self) -> tuple:
        """Get env variables from .env file

        Args:

        Returns:
            tuple: Tuple containing the email, password, and workspace ID from the .env file.
        """

        # Load environment variables from .env file
        load_dotenv()
        # Get the email and API key from environment variables
        email = getenv("TOGGL_USERNAME")
        password = getenv("TOGGL_PASSWORD")
        organization_id = getenv("TOGGL_ORGANIZATION_ID")
        return email, password, organization_id

    def _create_headers(self):
        """Create request headers with authorization credentials
        Args:

        Returns:
            dictionary containing request headers
        """

        auth = b64encode(f"{self.email}:{self.password}".encode("ascii")).decode("ascii")
        return {"content-type": "application/json", "Authorization" : f"Basic {auth}"}

    def _split_date_range(self, start_date: str, end_date: str) -> list:
        """Splits a date range into increments where each increment ends on the last day of the year
        of the start date, if the range is larger than 365 days.

        Args:
            start_date (str): Start date in "YYYY-MM-DD" format.
            end_date (str): End date in "YYYY-MM-DD" format.

        Returns:
            list: List of tuples containing the split date ranges.
        """

        # Validate start and end date are in the correct format
        date_pattern = r"^\d{4}\-\d{2}\-\d{2}$"
        if not re.match(date_pattern, start_date):
            raise ValueError(f"Invalid start date format: {start_date}")
        if not re.match(date_pattern, end_date):
            raise ValueError(f"Invalid start date format: {end_date}")

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        result = []
        start_year = start.year
        end_year = end.year
        # Check if range between start and end date is larger than 365 days
        # If so, break up range into yearly tuples
        if (end - start).days > 365:
            for y in range(start_year, end_year + 1):
                if y != end_year:
                    if y != start_year:
                        sd = start.replace(year=y, month=1, day=1)
                    else:
                        sd = start
                    ed = end.replace(year=y, month=12, day=31)
                else:
                    sd = start.replace(year=y, month=1, day=1)
                    ed = end
                result.append((sd.strftime("%Y-%m-%d"), ed.strftime("%Y-%m-%d")))
        else:
            result.append((start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))

        return result

    def _parse_data(self, data: list) -> list:
        """Parse the data fetch from the Toggl API

            Args:
                data (list): List of dictionaries containing the data fetch from the API

            Returns:
                parsed_data (list): List of dictionaries containing the parsed data
        """

        parsed_data = []
        for batch in data:
            for entry in batch:
                row_dict = {
                    "user_id": entry.get("user_id"),
                    "username": entry.get("username"),
                    "project_id": entry.get("project_id"),
                    "task_id": entry.get("task_id"),
                    "billable": entry.get("billable"),
                    "description": entry.get("description"),
                    "tag_ids": entry.get("tag_ids"),
                    "billable_amount_in_cents": entry.get("billable_amount_in_cents"),
                    "hourly_rate_in_cents": entry.get("hourly_rate_in_cents"),
                    "currency": entry.get("currency"),
                    "id": entry.get("time_entries")[0].get("id"),
                    "seconds": entry.get("time_entries")[0].get("seconds"),
                    "start": entry.get("time_entries")[0].get("start"),
                    "stop": entry.get("time_entries")[0].get("stop"),
                    "at": entry.get("time_entries")[0].get("at"),
                    "at_tz": entry.get("time_entries")[0].get("at_tz"),
                }
                parsed_data.append(row_dict)
        return parsed_data

    def get_organization(self) -> dict:
        """Get organization metadata from Toggl API

        Returns:
            dictionary containing organization metadata
        """

        return requests.get(f"{self.base_url}/api/v9/organizations/{self.organization_id}", headers=self.headers).json()

    def get_workspace_ids(self) -> list:
        """Fetch the workspace id's from the Toggl API given an organization_id.

        Args:

        Returns:
            list of workspace_ids
        """

        workspace_url = f"{self.base_url}/api/v9/organizations/{self.organization_id}/workspaces/statistics"
        return list(requests.get(workspace_url, headers=self.headers).json().keys())

    def get_projects(self, workspace_id: str) -> list:
        """Get project metadata from Toggl API
    
        Args:
            workspace_id (str): ID of the Toggl workspace

        Returns:
            list of dictionaries containing project metadata
        """

        return requests.get(f"{self.base_url}/api/v9/workspaces/{workspace_id}/projects", headers=self.headers).json()

    def get_workspace(self, workspace_id: str) -> dict:
        """Get workspace metadata from Toggl API

        Args:
            workspace_id (str): ID of the Toggl workspace

        Returns:
            dictionary containing workspace metadata
        """

        return requests.get(f"{self.base_url}/api/v9/workspaces/{workspace_id}", headers=self.headers).json()


    def fetch_data(self, workspace_id: str, start_date: str, end_date:str) -> list:
        """Fetch time entry data from the Toggl API. The API has limit of 30 calls per hour and maximum allowed date range is 366 days.
        Docs: https://engineering.toggl.com/docs/reports/detailed_reports/

            Args:
                start_date (str): Start date in "YYYY-MM-DD" format.
                end_date (str): End date in "YYYY-MM-DD" format.

            Returns:
                data_list (list): List of dictionaries containing the data fetch from the API
        """

        data_list = []
        date_ranges = self._split_date_range(start_date=start_date, end_date=end_date)
        for date_range in date_ranges:
            start_date, end_date = date_range
            logger.info(f"Fetching data for {start_date} to {end_date} for workspace id {workspace_id}")
            data = requests.post(
                        url=f"{self.base_url}/reports/api/v3/workspace/{workspace_id}/search/time_entries",
                        json={
                            "start_date": start_date,
                            "end_date": end_date,
                            "page_size": 5000,
                            # "first_row_number": 11,
                        },
                        headers=self.headers
                    ).json()
            data_list.append(data)
            logger.info(f"Fetched {len(data)} row(s) of data")

        return self._parse_data(data=data_list)
