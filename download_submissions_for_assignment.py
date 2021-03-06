# Import the Canvas class
from canvasapi import Canvas
from pathlib import Path
import urllib, zipfile, shutil

import localcanvasapi

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    download_submissions(canvas, args.course, args.assignment, args.user)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Download a zip file with all of the submissions for an assignment in a course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-a', '--assignment', required=True, help='The assignment id for the submissions desired')
    p.add_argument('-u', '--user', help='the username of the single user whose submissions are desired')
    return p

def download_submissions(canvas: Canvas, course_id: str, assignment_id: str, user=None):
    course = canvas.get_course(course_id)
    assignment = course.get_assignment(assignment_id)
    for s in assignment.get_submissions(include=['user', 'submission_history']):
        username = s.user['sortable_name']
        for h in s.submission_history:
            if(h['attempt']):
                print(f"\n{username} {h['attempt']} {h['submitted_at']} {h['workflow_state']} {h['submission_type']}")
                if(user == None or (user and user.lower() == s.user['login_id'].lower())):
                    print(f"Downloading {assignment.name}-{h['attempt']} for {username}")
                    path = Path(f'{assignment.name}/{username}-{h["attempt"]}')
                    path.mkdir(parents=True, exist_ok=True) #make a directory with the assignment name and username
                    if('attachments' in h):
                        for a in h['attachments']:
                            try:
                                filepath = path.joinpath(a['filename'])
                                with urllib.request.urlopen(a['url']) as response, open(filepath, 'wb') as out_file:
                                    data = response.read() # a `bytes` object
                                    out_file.write(data)
                                if(a['mime_class'] == 'zip'):
                                    with zipfile.ZipFile(filepath, 'r') as zip_ref:
                                        zip_ref.extractall(path)
                                    #copy exe, txt, and form1.cs
                                    copy_debug_dir_to_top(path, "**/bin/Debug")
                                    copy_files_in_tree_to_top(path, "**/Form1.cs")
                            except Exception as e:
                                print(f'unable to download attachment for {assignment.name}-{s.attempt} for {username}')
                                print(e)

def copy_files_in_tree_to_top(path: Path, glob: str):
    for f in list(path.glob(glob)):
        shutil.copy(f,path)

def copy_debug_dir_to_top(path: Path, glob: str):
    for f in list(path.glob(glob)):
        print(f'copying {f} to {path}')
        shutil.copytree(f, path, dirs_exist_ok=True)

if __name__ == '__main__':
   main()