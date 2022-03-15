from canvasapi import Canvas
from highlight import highlight_file
from update_page import update_page

import localcanvasapi

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    page_contents = highlight_file(args.file, args.type, encoding=args.encoding)
    update_page(canvas, args.course, None, args.page_title, page_contents)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "Create or update a page.  --page_title is required when creating, and page_url is required when updating"
    p.add_argument('-c', '--course', required=True, help='The course id whose events will be listed or deleted')
    p.add_argument('-p', '--page_title', help='The name of the page to create')    
    p.add_argument('-f', '--file', required=True, help='The file containing the source code to highlight and upload')
    p.add_argument('-t', '--type', required=True, help='the source code type to use for highlighting (e.g., c#, py)')
    p.add_argument('-e', '--encoding', default='utf_8_sig', help='the file encoding (defaults to utf_8_sig, which works for visual studio on windows)')
    return p
    
if __name__ == '__main__':
   main()