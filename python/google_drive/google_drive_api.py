from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2 import service_account


class GoogleSheetsApi:
    """Class to interact with Google Sheets API
    """

    def __init__(self, key_file_location):
        """Instantiate GoogleSheetsApi
        """
        self.key_file_location = key_file_location
        self.scopes = [
            "https://www.googleapis.com/auth/drive.metadata.readonly",
            "https://www.googleapis.com/auth/spreadsheets.readonly",
        ]
        self.credentials = self._get_credentials()
        self.drive_service = self.get_drive_service()
        self.sheets_service = self.get_sheets_service()

    def _get_credentials(self):
        """Get credentials for Google Sheets API

        Args:

        Returns:
            credentials: OAuth2 service account credentials object

        """

        credentials = service_account.Credentials.from_service_account_file(
            self.key_file_location
        )
        return credentials


    def get_drive_service(self):
        """Get a service that communicates to the Google Drive API.

        Args:

        Returns:
            A service that is connected to the Google Drive API.

        """

        scoped_credentials = self.credentials.with_scopes(
            self.scopes
        )
        # Build the service object.
        service = build(
            "drive",
            "v3",
            credentials=scoped_credentials
        )
        return service

    def get_sheets_service(self):
        """Get a service that communicates to the Google Sheets API.

        Args:

        Returns:
            A service that is connected to the Google Sheets API.

        """

        scoped_credentials = self.credentials.with_scopes(
            self.scopes
        )
        # Build the service object.
        service = build(
            "sheets",
            "v4",
            credentials=scoped_credentials
        )
        return service

    def get_spreadsheet_ids(self):
        """Get list of spreadsheets user has access to

        Args:

        Returns:
            items (list): List of dictionaries of spreadsheets

        """

        # Call the Drive v3 API
        results = self.drive_service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name)"
        ).execute()
        items = results.get("files", [])
        return items


    def get_sheets_data(self, spreadsheet_id):
        """Get sheets data from a specific spreadsheet

        Args:
            spreadsheet_id (str): Google Sheets spreadsheet id

        Returns:
            values (list): Nested list of rows from spreadsheet

        """

        try:

            # Call the Sheets API
            sheet = self.sheets_service.spreadsheets()
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range="A:P"
            ).execute()
            values = result.get("values", [])

            if not values:
                print("No data found.")
                return

        except HttpError as err:
            print(err)

        else:
            return values


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """

    gsa = GoogleSheetsApi(
        key_file_location="key.json"
    )

    sheets = gsa.get_spreadsheet_ids()
    for sheet in sheets:
        if sheet.get("name") == "book_db":
            book_db_sheet_id = sheet.get("id")

    spreadsheet_values = gsa.get_sheets_data(
        spreadsheet_id=book_db_sheet_id
    )
    print(spreadsheet_values)

if __name__ == "__main__":
    main()
