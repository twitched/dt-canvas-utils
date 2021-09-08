# Import the Canvas class
from canvasapi import Canvas
from pathlib import Path
import urllib, zipfile, shutil

import localcanvasapi

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    download_submissions(canvas, args.course, args.assignment)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Download a zip file with all of the submissions for an assignment in a course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-a', '--assignment', required=True, help='The assignment id for the submissions desired')
    return p

def download_submissions(canvas: Canvas, course_id: str, assignment_id: str):
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)
    for s in assignment.get_submissions(include=['user']):
        if(s.attempt):
            print(vars(s))
            username = s.user['name']
            path = Path(f'{assignment.name}/{username}')
            path.mkdir(parents=True, exist_ok=True) #make a directory with the assignment name and username
            if(hasattr(s, 'attachments')):
                for a in s.attachments:
                    filepath = path.joinpath(a['filename'])
                    with urllib.request.urlopen(a['url']) as response, open(filepath, 'wb') as out_file:
                        data = response.read() # a `bytes` object
                        out_file.write(data)
                    if(a['mime_class'] == 'zip'):
                        with zipfile.ZipFile(filepath, 'r') as zip_ref:
                            zip_ref.extractall(path)
                        #copy exe, txt, and form1.cs
                        copy_files_in_tree_to_top(path, "**/bin/**/*.exe")
                        copy_files_in_tree_to_top(path, "**/bin/**/*.txt")
                        copy_files_in_tree_to_top(path, "**/Form1.cs")

def copy_files_in_tree_to_top(path: Path, glob: str):
    for f in list(path.glob(glob)):
        shutil.copy(f,path)

if __name__ == '__main__':
   main()