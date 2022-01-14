# Import the Canvas class
from canvasapi import Canvas, submission
from canvasapi.conversation import Conversation
from canvasapi.course import Course
import pandas as pd

import localcanvasapi

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    submissions = get_grades(canvas, args.course, args.student, args.assignments)
    df = get_grades_data_frame(submissions)
    df.sort_values(['user.sortable_name', 'assignment.name'])
    if(args.reducedoutput):
        df = df[['assignment_id', 'assignment.name', 'user_id', 'user.name', 'score', 'late', 'excused', 'missing', 'points_deducted']]
    if(args.file):
        df.to_csv(args.file)
    else:
        print(df)
        
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "send a message to a recipient"
    p.add_argument('-c', '--course', required=True, help='the course context of the desired messages')
    p.add_argument('-u', '--student', help="provide a search string to get grades for a set of students.  If not given all students will be returned")
    p.add_argument('-a', '--assignments', help="get grades for all assignments that start with the given string.  If not given, all assignments will be returned")
    p.add_argument('-f', '--file', help="a csv file to write the result to")
    p.add_argument('-r', '--reducedoutput', action="store_true", help="only outputs assignment, user, and score.  Without this it outputs everything")
    return p

def get_grades(canvas: Canvas, course_id: str, student_search_string: str = None, assignment_search_string: str = None):
    """
        returns a list of submissions with each submission as a dictionary
    """
    course = canvas.get_course(course_id)
    assignments = search_assignments(course, assignment_search_string) if assignment_search_string != None else None
    students = get_students(course, student_search_string) if student_search_string != None else get_all_students(course)
    assignment_ids = [a.id for a in assignments] if assignments else None
    student_ids = [s.id for s in students]
    student_logins = [s.login_id.lower() for s in students]
    submissions = course.get_multiple_submissions(student_ids = student_ids, assignment_ids = assignment_ids, include=['user', 'assignment'])
    return [vars(s) for s in submissions]

def get_grades_data_frame(submissions):
    return pd.DataFrame(pd.json_normalize(submissions)).drop(columns=['_requester'])
        
def search_assignments(course: Course, search_string: str):
    return [a for a in course.get_assignments() if a.name.startswith(search_string)]

def get_students(course: Course, search_string: str):
    return [s for s in course.get_users(search_term = search_string, sort='username', enrollment_type = ['student', 'student_view'])]

def get_all_students(course: Course):
    return [s for s in course.get_users(sort='username', enrollment_type = ['student', 'student_view'])]

if __name__ == '__main__':
   main()