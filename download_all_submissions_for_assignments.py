# Import the Canvas class
from canvasapi import Canvas, exceptions

import localcanvasapi
import download_submissions_for_assignment

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    download_submissions(canvas, args.course, args.starts_with, args.user)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List all of the assignments in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('--starts_with', required=True, help='downloads all submissions from all assignments that start with this string')
    p.add_argument('-u', '--user', help='the username of the single user whose submissions are desired')
    return p

def download_submissions(canvas: Canvas, course_id: str, starts_with: str, user: str):
    course = canvas.get_course(course_id)
    for a in course.get_assignments():
        if(a.name.startswith(starts_with)):
            download_submissions_for_assignment.download_submissions(canvas, course_id, a.id, user)
    
if __name__ == '__main__':
   main()