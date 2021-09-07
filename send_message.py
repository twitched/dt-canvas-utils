# Import the Canvas class
from canvasapi import Canvas, exceptions, requester

import localcanvasapi

localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    send_message(canvas, args.recipient, args.subject, args.message)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "send a message to a recipient"
    p.add_argument('-r', '--recipient', required=True, help='The recipient id is a user id or a course, group, or section id prefixed with "course", "group" or "section"')
    p.add_argument('-u', '--subject', help="the message subject")
    p.add_argument('-m', '--message', required=True, help="The body of the message")
    return p

def send_message(canvas: Canvas, recipient_id: str, subject: str, message:str):
    canvas.create_conversation([recipient_id], message, subject=subject)
    
if __name__ == '__main__':
   main()