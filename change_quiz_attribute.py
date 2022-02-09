# Change quiz attributes.  For a list of attributes to change see https://canvas.instructure.com/doc/api/quizzes.html

from canvasapi import Canvas, exceptions

import localcanvasapi
import list_quizzes

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    change_quizzes(canvas, args.course, args.search_term, args.name, args.value)
    
def getargparser():
    p = list_quizzes.getargparser()
    p.description = "change an attribute of quizzes"
    p.add_argument('-n', '--name', required=True, help='the name of the attribute to change')
    p.add_argument('-v', '--value', required=True, help='the value to change the attribute to')
    return p

def change_quizzes(canvas: Canvas, course_id: str, search_term: str, name: str, value: str):
    course = canvas.get_course(course_id)
    kwargs = {}
    kwargs['search_term'] = search_term if search_term else None
    for q in course.get_quizzes(**kwargs):
        print(f'changing {name} to {value} on Quiz {q.title}')
        change_args = {}
        change_args[name] = bool(value)
        change_args['notify_of_update'] = False
        q.edit(quiz = change_args)
    
if __name__ == '__main__':
   main()