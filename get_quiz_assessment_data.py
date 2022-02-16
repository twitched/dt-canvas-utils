import csv, jmespath, keyring
from canvasapi import Canvas


############ Variables  ################
course_id = '12017'
quiz_name = 'Syllabus'
output_csv_file = 'syllabus.csv'
default_url = 'https://boisestatecanvas.instructure.com'
########################################

def main():
    canvas = get_canvas()
    course = canvas.get_course(course_id)
    kwargs = {}
    kwargs['search_term'] = quiz_name if quiz_name else None
    out = {"quizzes": [{"statistics" : [{"question_statistics" : s.question_statistics} for s in a.get_statistics()]} for a in course.get_quizzes(**kwargs)]}
    data = jmespath.search('quizzes[].statistics[].question_statistics[].{Text: question_text, Total_Responses: responses, Correct_responses: answers[?correct].responses | [0]}', out)

    #write it to a file
    with open(output_csv_file, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, ['Text', 'Total_Responses', 'Correct_responses'])
        writer.writeheader()
        writer.writerows(data)

def get_canvas():
    secrets = get_secrets()
    return Canvas(secrets['CANVAS_API_URL'], secrets['CANVAS_API_KEY'])

def get_secrets():
    secrets = {}
    secrets['CANVAS_API_URL'] = keyring.get_password("canvas", "url")
    secrets['CANVAS_API_KEY'] = keyring.get_password("canvas", "token")
    if(secrets['CANVAS_API_URL'] == None or secrets['CANVAS_API_KEY'] == None):
        print('Please enter the Canvas URL [hit enter to accept https://boisestatecanvas.instructure.com]:')
        url = input()
        if(url == '' or url == None):
            url = default_url
        print('Please enter your Canvas API Secret Token:')
        token = input()
        keyring.set_password('canvas', 'url', url)
        keyring.set_password('canvas', 'token', token)
        secrets['CANVAS_API_URL'] = keyring.get_password("canvas", "url")
        secrets['CANVAS_API_KEY'] = keyring.get_password("canvas", "token") 
    return secrets

if __name__ == '__main__':
   main()