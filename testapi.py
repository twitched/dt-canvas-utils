import os, sys, json
# Import the Canvas class
from canvasapi import Canvas

itm455 = 3614

def main():
    canvas = startcanvasapi()
    test_connection(canvas)
    test_graphql(canvas)
    get_graphql_schema(canvas)

# Read the URL and KEY from a file and create and return a Canvas API object
def startcanvasapi() -> Canvas:
    # Canvas API URL
    secrets_dict = {}
    secrets_file = open('secrets', 'r')
    for line in secrets_file:
        key, value = line.split('=')
        secrets_dict[key] = value
    return Canvas(secrets_dict['CANVAS_API_URL'], secrets_dict['CANVAS_API_KEY'])


#see if we get a course
def test_connection(canvas: Canvas):
    course = canvas.get_course(itm455)
    print(course.name)
    
def test_graphql(canvas: Canvas):
    out = canvas.graphql('''query courseInfo($courseId: ID!) {
       course(id: $courseId) {
        id
        _id
        name
        }
       }
     }''', variables={'courseId': itm455})
    print(json.dumps(out))

def get_graphql_schema(canvas: Canvas):
    out = canvas.graphql(
        '''{
                __schema {
                    mutationType {
                      name
                    }
                }
            }''')
    print(json.dumps(out, sort_keys=True, indent=2))