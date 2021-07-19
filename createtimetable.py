import os, sys, json, csv, datetime, pytz
from typing import IO
# Import the Canvas class
from canvasapi import Canvas, util
from canvasapi.requester import Requester
from canvasapi.util import combine_kwargs

# We will get these via argparse later
course = 3614 #itm455 for now
timetable_file = "schedule_test.csv"
timezone = pytz.timezone('America/Boise')
secrets_file = 'secrets'

import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG) #debug for now

def main():
    secrets = read_secrets(secrets_file)
    canvas = startcanvasapi()
    create_timetable(secrets, read_timetable_from_csv(timetable_file), course)

# Read the URL and KEY from a file and create and return a Canvas API object
def startcanvasapi() -> Canvas:
    # Canvas API URL
    secrets = read_secrets(secrets_file)
    return Canvas(secrets['CANVAS_API_URL'], secrets['CANVAS_API_KEY'])

def read_secrets(secrets_file: str) -> dict:
    secrets_dict = {}
    secrets_file = open(secrets_file, 'r')
    for line in secrets_file:
        key, value = line.split('=')
        secrets_dict[key.strip()] = value.strip() 
    return secrets_dict   
        
def combine_date_time_zone(date: str, time: str, zone: pytz) -> datetime.datetime:
    return zone.localize(datetime.datetime.strptime(f"{date} {time}", "%m/%d/%y %I:%M %p"))
    
# Read from csv to json
def read_timetable_from_csv(file: IO) -> dict:
    return csv.DictReader(file)        

def create_timetable(secrets, timetable: dict, course: int):
    tt = read_timetable_from_csv(open(timetable_file, 'r', encoding='utf-8-sig'))
    events = []
    for row in tt:
        events.append({
            'start_at': combine_date_time_zone(row['date'], row['start_time'], timezone).isoformat(),
            'end_at': combine_date_time_zone(row['date'], row['end_time'], timezone).isoformat(),
            'location_name': row['location'],
            'title': f"ITM 455 - {row['title']}",
            'description': '<h1>TEst</h1>'
        })
    print(json.dumps({'events': events}, indent=2)) 
    requester = Requester(secrets['CANVAS_API_URL'].strip(), secrets['CANVAS_API_KEY'].strip())
    resp = requester.request('POST', f'courses/{course}/calendar_events/timetable_events', _kwargs=combine_kwargs(**{'events': events}))
    print(resp) 
  
if __name__ == '__main__':
   main()