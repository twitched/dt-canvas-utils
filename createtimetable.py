import csv, datetime, pytz
from typing import IO
# Import the Canvas class
from canvasapi import Canvas
from canvasapi.requester import Requester
from canvasapi.util import combine_kwargs
import localcanvasapi

localcanvasapi.debug()

def main():
    args = getargs()
    args.parse_args()
    secrets = localcanvasapi.read_secrets(args.secrets)
    create_timetable(secrets, read_timetable_from_csv(args.timetable), args.course, args.timezone)
    
def getargs():
    p = localcanvasapi.get_argparser()
    p.add_argument('-c', '--course', required=True, help='The course number to add the timetable to')
    p.add_argument('-t', '--timetable', required=True, help='The file containing the timetable.  See Documentation')
    p.add_argument('-z', '--timezone', default = 'America/Boise', help='The timezone of the events')
    return p
        
def combine_date_time_zone(date: str, time: str, zone: pytz) -> datetime.datetime:
    return zone.localize(datetime.datetime.strptime(f"{date} {time}", "%m/%d/%y %I:%M %p"))
    
# Read from csv to json
def read_timetable_from_csv(file: IO) -> dict:
    return csv.DictReader(file)        

def create_timetable(secrets, timetable_file: str, course: int, timezone: str):
    tt = read_timetable_from_csv(open(timetable_file, 'r', encoding='utf-8-sig'))
    events = []
    for row in tt:
        events.append({
            'start_at': combine_date_time_zone(row['date'], row['start_time'], timezone).isoformat(),
            'end_at': combine_date_time_zone(row['date'], row['end_time'], timezone).isoformat(),
            'location_name': row['location'],
            'title': f"ITM 455 - {row['title']}",
        })
    requester = Requester(secrets['CANVAS_API_URL'].strip(), secrets['CANVAS_API_KEY'].strip())
    resp = requester.request('POST', f'courses/{course}/calendar_events/timetable_events', _kwargs=combine_kwargs(**{'events': events}))
    print(resp) 

if __name__ == '__main__':
   main()