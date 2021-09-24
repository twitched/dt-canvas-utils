# Import the Canvas class
from canvasapi import Canvas, exceptions

import localcanvasapi

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    list_assignments(canvas, args.course, args.search_term)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List all of the assignments in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-t', '--search_term', help='optional search term to limit which assignments are listed')
    return p

def list_assignments(canvas: Canvas, course_id: str, search_term: str):
    course = canvas.get_course(course_id)
    kwargs = {}
    kwargs['search_term'] = search_term if search_term else None
    for a in course.get_assignments(**kwargs):
        print(a)
    
if __name__ == '__main__':
   main()