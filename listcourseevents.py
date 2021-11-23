# Import the Canvas class
from canvasapi import Canvas

import localcanvasapi

localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    if(args.delete):
        delete_all_events(get_all_events(canvas, args.course))
    else:
        list_all_events(get_all_events(canvas, args.course))
    
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List or delete all events in a course"
    p.add_argument('-c', '--course', required=True, help='The course whose events will be listed or deleted')
    p.add_argument('-d', '--delete', action='store_true', help='permanently DELETES all events in the course')
    return p
        
def get_all_events(canvas: Canvas, course: str):
    return canvas.get_calendar_events(context_codes = [f'course_{course}'], all_events = 'true')

def list_all_events(events):
    for event in events:
        print(event)

def delete_all_events(events):
    for event in events:
        print(f'deleting {event}')
        event.delete()

if __name__ == '__main__':
   main()