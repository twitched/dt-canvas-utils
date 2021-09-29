# Import the Canvas class
from typing import IO
from canvasapi import Canvas
import argparse

from canvasapi.user import User

import localcanvasapi

localcanvasapi.debug()

conversation_upload_folder = 'conversation attachments'

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    if(args.attachment):
        send_message_with_attachment(canvas, args.recipient, args.subject, args.message, args.force_new, args.attachment)
    else:
        send_message(canvas, args.recipient, args.subject, args.message, args.force_new)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "send a message to a recipient"
    p.add_argument('-r', '--recipient', required=True, help='The recipient id is a user id or a course, group, or section id prefixed with "course", "group" or "section"')
    p.add_argument('-b', '--subject', help="the message subject")
    p.add_argument('-m', '--message', required=True, help="The body of the message")
    p.add_argument('-n', '--force_new', action='store_true', help='force a new conversation instead of adding to previous')
    p.add_argument('-a', '--attachment', type=argparse.FileType('r', encoding='utf-8'))
    return p

def send_message(canvas: Canvas, recipient_id: str, subject: str, message:str, force_new: bool):
    canvas.create_conversation([recipient_id], message, subject=subject, force_new=force_new)

def send_message_with_attachment(canvas: Canvas, recipient_id: str, subject: str, message:str, force_new: bool, attachment: IO, sender: User = None):
    if(sender == None):
        sender = canvas.get_current_user()
    attached = sender.upload(attachment, parent_folder_path='conversation attachments')
    if(attached[0]):
        canvas.create_conversation([recipient_id], message, subject=subject, force_new=force_new, attachment_ids = [attached[1]['id']])
    else:
        print("attachment upload unsuccessful.  Retry with localcanvasapi.debug()")
    
if __name__ == '__main__':
   main()