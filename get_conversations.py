# Import the Canvas class
from canvasapi import Canvas
from canvasapi.conversation import Conversation

import localcanvasapi

#localcanvasapi.debug()

def main():
    args = getargparser().parse_args()
    canvas = localcanvasapi.startcanvasapi(args)
    get_messages(canvas, args.course, args.subject)
    
def getargparser():
    p = localcanvasapi.get_argparser()
    p.description = "send a message to a recipient"
    p.add_argument('-c', '--course', help='the course context of the desired messages')
    p.add_argument('-u', '--subject', help="the subject of the desired messages")
    return p

def get_messages(canvas: Canvas, course = None, subject = None):
    conversations = canvas.get_conversations(filter = [course, subject], filter_mode = 'and')
    for conv in conversations:
        print(str(vars(conv)) + '\n')
        conversation = canvas.get_conversation(conv)
        for message in conversation.messages:
            print(str(message) + '\n')
            print(message['body'])
            for attachment in message['attachments']:
                print(attachment['url'])
        print('\n--------\n')
    
if __name__ == '__main__':
   main()