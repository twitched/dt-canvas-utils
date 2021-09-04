# Import the Canvas class
from typing import IO
from canvasapi import Canvas
import argparse, csv

import localcanvasapi

localcanvasapi.debug() 

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    print(args)
    if(args.file):
        save_users(canvas, args.course, args.file)
    else:
        list_users(canvas, args.course)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List all of the assignments in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-f', '--file', type=argparse.FileType('w', encoding='utf-8'), help="If present, all student information will be saved as a csv to the given file")
    return p

def list_users(canvas: Canvas, course_id: str):
    course = canvas.get_course(course_id)
    for a in course.get_users():
        print(a)
        
def save_users(canvas: Canvas, course_id: str, file: IO):
    course = canvas.get_course(course_id)
    users = course.get_users()
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