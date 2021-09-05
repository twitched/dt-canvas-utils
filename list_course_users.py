# Import the Canvas class
from typing import IO
from canvasapi import Canvas
import argparse, csv

import localcanvasapi

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    enrollment_types = []
    if(args.students):
        enrollment_types.append('student')
    if(args.test_student):
        enrollment_types.append('student_view')
    if(args.file):
        save_users(canvas, args.course, args.file, enrollment_types)
    else:
        list_users(canvas, args.course, enrollment_types)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List all of the assignments in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-t', '--test_student', action='store_true', help='include the test student')
    p.add_argument('--students', action='store_true', help='only include students')
    p.add_argument('-f', '--file', type=argparse.FileType('w', encoding='utf-8'), help="If present, all student information will be saved as a csv to the given file")
    return p

def list_users(canvas: Canvas, course_id: str, enrollment_types: list[str]):
    course = canvas.get_course(course_id)
    for a in course.get_users(enrollment_type = enrollment_types):
        print(a)
        
def save_users(canvas: Canvas, course_id: str, file: IO, enrollment_types: list[str]):
    course = canvas.get_course(course_id)
    users = course.get_users(enrollment_type = enrollment_types)
    first = True
    out = csv.DictWriter(file, ['id', 'name', 'created_at', 'sortable_name', 'short_name', 'sis_user_id', 'integration_id', 'login_id', 'email', 'pronouns'])
    out.writeheader()
    for u in users:
        row = vars(u)
        row.pop('_requester')
        out.writerow(row)
    file.close()
    
if __name__ == '__main__':
   main()