import csv
from typing import IO
# Import the Canvas class
from canvasapi import Canvas
import localcanvasapi

#localcanvasapi.debug()

def main():
    args = getargs().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    submit_grades(canvas, args.course, args.assignment_starts_with)
    
    
def getargs():
    p = localcanvasapi.get_argparser()
    p.add_argument('-c', '--course', required=True, help='The course number to add the timetable to')
    p.add_argument('-a', '--assignment_starts_with', required=True, help='assignments that start with this will be included')
    return p
        
def submit_grades(canvas: Canvas, course_id: str, assignment_starts_with: str):
    course = canvas.get_course(course_id)
    kwargs = {}
    kwargs['search_term'] = assignment_starts_with if assignment_starts_with else None
    for a in course.get_assignments(**kwargs):
        for s in a.get_submissions():
            if(s.excused != True and s.missing == True and s.submitted_at == None):
                print(f'late_policy_status: {s.late_policy_status}, late {s.late}, missing {s.missing}, submittted_at {s.submitted_at}')
                s.edit(submission={'assignment_id': a.id, 'user_id': s.user_id, 'late_policy_status': 'none'})
        
if __name__ == '__main__':
   main()