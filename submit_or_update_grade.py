import csv
from typing import IO
# Import the Canvas class
from canvasapi import Canvas
import localcanvasapi


def main():
    args = getargs().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    submit_grades(canvas, args.course, args.assignment, args.file)
    
    
def getargs():
    p = localcanvasapi.get_argparser()
    p.add_argument('-c', '--course', required=True, help='The course number to add the timetable to')
    p.add_argument('-a', '--assignment', required=True, help='the assignment id to submit to')
    p.add_argument('-f', '--file', required=True, help='file containting the grades.  One column must be "user_id", the other, "score"')
    return p
        
def submit_grades(canvas: Canvas, course_id: str, assignment_id: str, file: str):
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            user_id = row['user_id']
            score = row['score']
            prior_submission = assignment.get_submission(user_id)
            prior_submission.edit(submission = {'posted_grade': score} )

        
if __name__ == '__main__':
   main()