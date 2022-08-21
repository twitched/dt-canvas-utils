# Import the Canvas class
from canvasapi import Canvas

import localcanvasapi

localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    update_syllabus(canvas, args.course, open(args.file, mode ='r').read())
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Create or update a page.  --page_title is required when creating, and page_url is required when updating"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-f', '--file', required=True, help='The file containing the html of the page')
    return p

def update_syllabus(canvas: Canvas, course_id: str, contents: str):
    course = canvas.get_course(course_id)
    course.update(course={'syllabus_body': contents})

if __name__ == '__main__':
   main()