from canvasapi import Canvas
import localcanvasapi, csv, time

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    if(args.list):
        list_columns(canvas, args.course)
    elif(args.new):
        new_column(canvas, args.course, args.new, args.file)
    elif(args.delete):
        delete_column(canvas, args.course, args.delete)
    elif(args.update):
        update_column(canvas, args.course, args.update, args.file)
    
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
    course.create_custom_column(column={'title':title, 'read_only': 'true'})
    if(file):
        update_column(canvas, course.id, title, file)

def find_column_by_name(canvas: Canvas, course, title: str):
    for a in course.get_custom_columns():
        if(a.title == title):
            return a
    return None
        
def delete_column(canvas: Canvas, course_id: str, title: str):
    course = canvas.get_course(course_id)
    column = find_column_by_name(canvas, course, title)
    if(column):
        column.delete()
    else:
        print(f'could not find {column}')

def update_column(canvas: Canvas, course_id: str, title: str, file: str):
    course = canvas.get_course(course_id)
    column = find_column_by_name(canvas, course, title)
    if(column):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            bulk_column_data = []
            for row in reader:
                row_data = {'column_id': column.id, 'user_id': row['id'], 'content': row['content']}
                bulk_column_data.append(row_data)
        progress = course.column_data_bulk_update(bulk_column_data)
        while(progress.workflow_state != "completed"):
            print(f"waiting for bulk update...{progress.workflow_state}")
            time.sleep(.5)
            progress = progress.query()
        print("done")
        
    else:
        print(f'could not find {column}')
    
if __name__ == '__main__':
   main()