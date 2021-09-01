# Import the Canvas class
from canvasapi import Canvas, exceptions

import localcanvasapi

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    list_assignments(canvas, args.course)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Create or update a page.  --page_title is required when creating, and page_url is required when updating"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    return p

def list_assignments(canvas: Canvas, course_id: str):
    course = canvas.get_course(course_id)
    for a in course.get_assignments():
        print(a)
    
if __name__ == '__main__':
   main()