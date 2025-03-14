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

    def __init__(self) -> tuple:
        """Initialize the TogglAPI class"""
        self.email, self.password, self.workspace_id = self._get_env_variables()
        self.url = f"https://api.track.toggl.com/reports/api/v3/workspace/{self.workspace_id}/search/time_entries"

    def _get_env_variables(self):
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
        workspace_id = getenv("TOGGL_WORKSPACE_ID")
        return email, password, workspace_id

    def _split_date_range(self, start_date: str, end_date: str) -> list:
        """Splits a date range into increments where each increment ends on the last day of the month
        of the start date, if the range is larger than 30 days.

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
        while (end - start).days > 30:
            # Get the last day of the current month
            last_day_of_month = monthrange(start.year, start.month)[1]
            increment_end = datetime(start.year, start.month, last_day_of_month)
            # Ensure the increment end does not exceed the overall end date
            if increment_end > end:
                increment_end = end
            result.append((start.strftime('%Y-%m-%d'), increment_end.strftime('%Y-%m-%d')))
            start = increment_end + timedelta(days=1)

        # Add the final range if any
        if start <= end:
            result.append((start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')))
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


    def fetch_data(self, start_date: str, end_date:str) -> list:
        """Fetch data from the Toggl API

            Args:
                start_date (str): Start date in "YYYY-MM-DD" format.
                end_date (str): End date in "YYYY-MM-DD" format.

            Returns:
                data_list (list): List of dictionaries containing the data fetch from the API
        """

        auth = b64encode(f"{self.email}:{self.password}".encode("ascii")).decode("ascii")
        headers = {
            "content-type": "application/json",
            "Authorization" : f"Basic {auth}"
        }

        data_list = []
        date_ranges = self._split_date_range(start_date=start_date, end_date=end_date)
        for date_range in date_ranges:
            start_date, end_date = date_range
            logger.info(f"Fetching data for {start_date} to {end_date}")
            data = requests.post(
                        self.url,
                        json={
                            "start_date": start_date,
                            "end_date": end_date,
                            "page_size": 500,
                            # "first_row_number": 11,
                        },
                        headers=headers
                    ).json()
            data_list.append(data)
            logger.info(f"Fetched {len(data)} row(s) of data")

        return self._parse_data(data=data_list)
