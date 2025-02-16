import icalendar
from pathlib import Path

from typing import Optional, List, Union
from pymongo import MongoClient

import hashlib


def ics_extract_events(ics_path : Union[str,Path]) -> List:
    """
    Loads an ics file and extract subject and start/end times from all events.

    :param ics_path:
    :return: List with the event data.
    """

    if type(ics_path) == str:
        ics_path = Path(ics_path)

    with ics_path.open() as f:
        calendar = icalendar.Calendar.from_ical(f.read())

    events = []

    for event in calendar.walk('VEVENT'):
        events.append((event.get("SUMMARY"), event.get('DTSTART').dt, event.get('DTEND').dt))

    return events


def add_events(events: List, user_id : str, MongoDBclient: Optional[MongoClient] = None):
    """
    Adds a list of events to the MongoDB database. Also have duplicate detection.

    :param events:
    :param user_id:
    :param MongoDBclient:
    """

    if MongoDBclient is None:
        MongoDBclient = MongoClient('127.0.0.1', 27017)

    calendars = MongoDBclient["Hack"]["Calendars"]

    query = calendars.find_one({'_id': user_id})

    if query is not None:
        post_events = query['events']
        replace = True
    else:
        post_events = dict()
        replace = False

    appended = False

    for data in events:
        data_hash = hashlib.sha1(bytes(str(data), 'utf-8')).hexdigest()
        try:
            post_events[str(data_hash)]
        except KeyError:
            appended = True
            post_events[str(data_hash)] = data

    if appended:
        post = {'_id': user_id, 'events': post_events}
        print('Inserting:')
        print(post)
        if replace:
            calendars.replace_one({'_id': user_id}, post)
        else:
            calendars.insert_one(post)


def output_events(user_id : str, MongoDBclient: Optional[MongoClient] = None):
    if MongoDBclient is None:
        MongoDBclient = MongoClient('127.0.0.1', 27017)

    calendars = MongoDBclient["Hack"]["Calendars"]

    response = calendars.find({'_id': user_id})
    return [v for _,v in response[0]['events'].items()]


if __name__ == "__main__":
    ics_path = Path("./calendar.ics")
    user_id = '1354'

    events = ics_extract_events(ics_path)
    add_events(events, user_id)

    print(output_events(user_id))
