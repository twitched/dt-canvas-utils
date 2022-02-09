# Change quiz attributes.  For a list of attributes to change see https://canvas.instructure.com/doc/api/assignmentzes.html

from canvasapi import Canvas, exceptions

import localcanvasapi
import list_assignments

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    change_assignments(canvas, args.course, args.search_term, args.name, args.value)
    
def getargparser():
    p = list_assignments.getargparser()
    p.description = "change an attribute of assignments"
    p.add_argument('-n', '--name', required=True, help='the name of the attribute to change')
    p.add_argument('-v', '--value', required=True, help='the value to change the attribute to')
    return p

def change_assignments(canvas: Canvas, course_id: str, search_term: str, name: str, value: str):
    course = canvas.get_course(course_id)
    kwargs = {}
    kwargs['search_term'] = search_term if search_term else None
    for a in course.get_assignments(**kwargs):
        print(f'changing {name} to {value} on Assignment {a.title}')
        a.edit(assignment = {name : value, 'notify_of_update': False})
    
if __name__ == '__main__':
   main()