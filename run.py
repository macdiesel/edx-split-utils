from flask import Flask, Response, request
import split.api as API
from bson import Binary, Code
from bson.json_util import dumps

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/api/v1/courses")
def get_courses():
    courses = API.get_courses()
    return Response(dumps(courses), mimetype='application/json')

@app.route("/api/v1/structure")
def get_structure():
    structure = API.get_structure(request.args.get('id'))

    if structure is None:
        return (None, 404)
    else:
        return Response(dumps(structure), mimetype='application/json')




if __name__ == "__main__":
    app.run()