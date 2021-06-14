import os
# Import the Canvas class
from canvasapi import Canvas

# Canvas API URL
API_URL = os.environ.get("CANVAS_API_URL")
# Canvas API key
API_KEY = os.environ.get("CANVAS_API_KEY")

# Initialize a new Canvas object
canvas = Canvas(API_URL, API_KEY)

course = canvas.get_course(3614)

print(course.name)