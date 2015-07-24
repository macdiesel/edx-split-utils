from flask import Flask, Response, request, render_template
import split.api as API
from bson.json_util import dumps
from opaque_keys.edx.locator import CourseLocator


app = Flask(__name__)
app.debug = True


@app.route("/")
def hello():
    return render_template('split/templates/graphtest.html')


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


@app.route("/api/v1/structure_id/<course>")
def get_structure_id(course):
    course_key = CourseLocator.from_string(course)
    try:
        structure_id = API.get_structure_id(course_key)
    except API.CourseNotFound:
        return (None, 404)
    return Response(dumps(structure_id), mimetype='application/json')


@app.route("/api/v1/block_counts/<course>")
def get_course_block_counts(course):
    course_key = CourseLocator.from_string(course)
    try:
        structure_id = API.get_structure_id(course_key)
    except API.CourseNotFound:
        return (None, 404)
    counts = API.get_block_counts(structure_id)
    return Response(dumps(counts), mimetype='application/json')


@app.route("/api/v1/history/main/<course>")
def get_structure_history(course):
    course_key = CourseLocator.from_string(course)
    try:
        history = API.get_structure_history(course_key)
    except API.CourseNotFound:
        return (None, 404)
    return Response(dumps(history), mimetype='application/json')


@app.route("/api/v1/history/all/<course>")
def get_structure_history_graph(course):
    course_key = CourseLocator.from_string(course)
    try:
        root, history_graph = API.get_structure_history_graph(course_key)
    except API.CourseNotFound:
        return (None, 404)
    return Response(dumps(root, history_graph), mimetype='application/json')


@app.route("/graph_test")
def graph_test():
    return render_template("graphtest.html")

if __name__ == "__main__":
    app.run()
