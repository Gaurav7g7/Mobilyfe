import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

def main():
    """Shows basic usage of the Google Calendar API.
    Stores the event name, start time, and end time of all events up to May 10, 2025 in a list.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Specify the calendar ID of the calendar you want to access
        calendar_id = "905muuodgt59mjr7h9uigum2r1pomh01@import.calendar.google.com"

        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        time_max = "2025-05-10T23:59:59Z"
        print("Getting all events up to May 10, 2025")
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=now,
                timeMax=time_max,
                maxResults=2500,  # Increase maxResults to retrieve more events
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # List to store events
        events_list = []

        if not events:
            print("No upcoming events found.")
            return

        # Append event details to the list
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            summary = event.get("summary", "No title")
            events_list.append({"summary": summary, "start": start, "end": end})

        # Handle pagination if there are more events
        while "nextPageToken" in events_result:
            events_result = (
                service.events()
                .list(
                    calendarId=calendar_id,
                    timeMin=now,
                    timeMax=time_max,
                    maxResults=2500,
                    singleEvents=True,
                    orderBy="startTime",
                    pageToken=events_result["nextPageToken"],
                )
                .execute()
            )
            events = events_result.get("items", [])
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                end = event["end"].get("dateTime", event["end"].get("date"))
                summary = event.get("summary", "No title")
                events_list.append({"summary": summary, "start": start, "end": end})

        # Print the list of events
        for event in events_list:
            print(f"Event: {event['summary']}, Start: {event['start']}, End: {event['end']}")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
