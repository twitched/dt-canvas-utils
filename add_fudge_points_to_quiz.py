# Import the Canvas class
from canvasapi import Canvas

import localcanvasapi

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    add_fudge_points(canvas, args.course, args.search_term, args.points, args.dry_run)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List all of the quizzes in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-t', '--search_term', help='optional search term to limit which quizzes are listed')
    p.add_argument('-p', '--points', required=True, type=float, help='How  many points to add (or subtract) to the quizzes')
    p.add_argument('-d', '--dry_run', action='store_true', help="if given, doesn't actually change the points")
    return p

def add_fudge_points(canvas: Canvas, course_id: str, search_term: str, points: float, dry_run: bool):
    course = canvas.get_course(course_id)
    kwargs = {}
    kwargs['search_term'] = search_term if search_term else None
    for q in course.get_quizzes(**kwargs):
        print(f'Do you want to add {points} to all submissions of {q.title}?')
        ans = input().strip()
        if(ans.lower() == 'y'):
            for s in q.get_submissions():
                print(f"setting fudge ponts for {s.user_id}'s attempt {s.attempt} of {q.title}")
                if not dry_run:
                    s.update_score_and_comments(quiz_submissions = [{'attempt': s.attempt, 'fudge_points' : 5}])
                    print('success')
    
if __name__ == '__main__':
   main()