# Import the Canvas class
from canvasapi import Canvas, exceptions

import localcanvasapi

localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    update_page(canvas, args.course, args.page_url, args.page_title, args.file)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Create or update a page.  --page_title is required when creating, and page_url is required when updating"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-p', '--page_url', help='The page url (the last part of the URL after "pages/") of the page to update')
    p.add_argument('-t', '--page_title', help='The name of the page to create')    
    p.add_argument('-f', '--file', required=True, help='The file containing the html of the page')
    return p

def update_page(canvas: Canvas, course_id: str, page_url: str, page_title: str, file:str):
    contents = open(file, 'r').read()
    course = canvas.get_course(course_id)
    new_page = {'body': contents}
    if(page_url):
        p = course.get_page(page_url)
        print(p)
        p.edit(**{'wiki_page[body]': new_page['body']})
    else:
        new_page['title'] = page_title
        course.create_page(new_page)
    
if __name__ == '__main__':
   main()