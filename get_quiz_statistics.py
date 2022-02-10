# Import the Canvas class
from canvasapi import Canvas
import json
import localcanvasapi

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    list_quizzes(canvas, args.course, args.search_term, args.file)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List all of the quizzes in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-t', '--search_term', help='optional search term to limit which quizzes are listed')
    p.add_argument('-f', '--file', required=True, help='the json file to save the questions to')
    return p

def list_quizzes(canvas: Canvas, course_id: str, search_term: str, file: str):
    course = canvas.get_course(course_id)
    kwargs = {}
    kwargs['search_term'] = search_term if search_term else None
    for a in course.get_quizzes(**kwargs):
        out = [json.dumps(s.question_statistics, indent = 4) for s in a.get_statistics()]
    open(file, 'w', encoding='utf-8').writelines(out)

if __name__ == '__main__':
   main()