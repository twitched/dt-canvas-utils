from canvasapi import Canvas
import localcanvasapi

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    if(args.list):
        list_columns(canvas, args.course)
    elif(args.new):
        new_column(canvas, args.course, args.new, args.file)
    elif(args.delete):
        delete_column(canvas, args.course, args.delete)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Manipulate custom gradebook columns in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('-l', '--list', action='store_true', help='list all custom grade columns')
    g.add_argument('-n', '--new', help='create a new grade column with the given title')
    g.add_argument('-d', '--delete', help='delete the grade column with the given title')
    g.add_argument('-u', '--update', help='update the grade column with the given title')
    p.add_argument('-f', '--file', help='a csv file containing the column data for --new and --update.  It should have two columns: user_id, content')
    return p

def list_columns(canvas: Canvas, course_id: str):
    course = canvas.get_course(course_id)
    for a in course.get_custom_columns():
        print(a)
        
def new_column(canvas: Canvas, course_id: str, title: str, file: str):
    course = canvas.get_course(course_id)
    return course.create_custom_column(column={'title':title})

def find_column_by_name(canvas: Canvas, course_id: str, title: str):
    course = canvas.get_course(course_id)
    for a in course.get_custom_columns():
        if(a.title == title):
            return a
        else:
            return None
        
def delete_column(canvas: Canvas, course_id: str, title: str):
    column = find_column_by_name(canvas, course_id, title)
    if(column):
        column.delete()
    else:
        print(f'could not find {column}')
    
if __name__ == '__main__':
   main()