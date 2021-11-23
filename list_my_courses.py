# Import the Canvas class
from canvasapi import Canvas, exceptions

import localcanvasapi

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    list_courses(canvas)
    
def getargparser():
    return localcanvasapi.get_argparser()

def list_courses(canvas: Canvas):
    u = canvas.get_current_user()
    for c in u.get_courses():
        print(c)
    
if __name__ == '__main__':
   main()