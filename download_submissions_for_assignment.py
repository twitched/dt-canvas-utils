# Import the Canvas class
from canvasapi import Canvas, exceptions

import localcanvasapi

localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    download_submissions(canvas, args.course, args.assignment)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Download a zip file with all of the submissions for an assignment in a course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-a', '--assignment', required=True, help='The assignment id for the submissions desired')
    return p

def download_submissions(canvas: Canvas, course_id: str, assignment_id: str):
    course = canvas.get_course(course_id)
    for s in course.get_assignment(assignment_id).get_submissions():
        print(s)
    #Doesn't do what it should tathis point.
    
if __name__ == '__main__':
   main()