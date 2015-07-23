from flask import Flask, Response
app = Flask(__name__)

import split.api as API
from bson import Binary, Code
from bson.json_util import dumps

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/v1/courses")
def get_courses():
    courses = API.get_courses()
    return Response(dumps(courses), mimetype='application/json')


if __name__ == "__main__":
    app.run()