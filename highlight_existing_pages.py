# Import the Canvas class
from canvasapi import Canvas, exceptions
from list_pages import get_pages
from bs4 import BeautifulSoup
from highlight import highlight_string

import localcanvasapi

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    highlight_existing_pages(canvas, args.course, args.search_term)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "List all of the assignments in this course"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be highlighted')
    p.add_argument('-t', '--search_term', help='optional search term to limit which pages are listed')
    return p

def highlight_existing_pages(canvas: Canvas, course_id: str, search_term: str):
    pages = get_pages(canvas, course_id, search_term)
    for p in pages:
        new_page = highlight_page_content(p.show_latest_revision().body)
        if(new_page):
            print(f'highlighting {p}')
            p.edit(**{'wiki_page[body]': new_page})
        else:
            print(f'No unformatted code block found in {p}')

# highlights the content if there's a <pre><code> block and that block doesn't already have
# a span in it.  If there's not appropriate block, return None
def highlight_page_content(page_content: str):
    soup = BeautifulSoup(page_content, 'html.parser')
    #modifiy this code to find code segments
    if(soup.pre and soup.pre.code and not soup.pre.code.span):
        return highlight_string(str(soup.pre.code.string).strip())
    else:
        return None
    
if __name__ == '__main__':
   main()