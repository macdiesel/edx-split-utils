from flask import Flask, Response, request, render_template, abort, redirect, url_for
import split.api as API
from bson.json_util import dumps
from opaque_keys.edx.locator import CourseLocator


app = Flask(__name__)
app.debug = True

@app.route("/")
@app.route("/<course>")
def hello(course = "course-v1:edX+test105+2015_Q2"):
    return render_template('graphtest.html', course_name = course)


@app.route("/api/v1/courses", methods=['GET'])
def get_courses():
    courses = API.get_courses()
    return Response(dumps(courses), mimetype='application/json')

@app.route("/api/v1/course/<course_id>", methods=['GET'])
def get_courses_by_id(course_id):
    try:
        course = API.get_course_by_id(course_id)
    except API.CourseNotFound:
        abort(404)
    return Response(dumps(course), mimetype='application/json')

@app.route("/api/v1/structure_id/<course>", methods=['GET'])
def get_structure_id(course):
    course_key = CourseLocator.from_string(course)
    try:
        structure_id = API.get_structure_id(course_key)
    except API.CourseNotFound:
        abort(404)
    return Response(dumps(structure_id), mimetype='application/json')


@app.route("/api/v1/block_counts/<course>", methods=['GET'])
def get_course_block_counts(course):
    course_key = CourseLocator.from_string(course)
    try:
        structure_id = API.get_structure_by_key(course_key)
    except API.CourseNotFound:
        abort(404)
    counts = API.get_block_counts(structure_id)
    return Response(dumps(counts), mimetype='application/json')

@app.route("/api/v1/block_counts_by_id/<course_id>", methods=['GET'])
def get_course_block_counts_by_id(course_id):
    try:
        structure_id = API.get_structure(course_id)
    except API.CourseNotFound:
        abort(404)
    counts = API.get_block_counts(structure_id['_id'])
    return Response(dumps(counts), mimetype='application/json')


@app.route("/api/v1/block_counts_by_structure/<struct_id>")
def get_block_counts_by_structure(struct_id):
    counts = API.get_block_counts(struct_id)
    return Response(dumps(counts), mimetype='application/json')


@app.route("/api/v1/history/main/<course>", methods=['GET'])
def get_structure_history(course):
    course_key = CourseLocator.from_string(course)
    try:
        history = API.get_structure_history(course_key)
    except API.CourseNotFound:
        abort(404)
    return Response(dumps(history), mimetype='application/json')


@app.route("/api/v1/history/all/<course>", methods=['GET'])
def get_structure_history_graph(course):
    course_key = CourseLocator.from_string(course)
    try:
        history_graph = API.get_structure_history_graph(course_key)
    except API.CourseNotFound:
        abort(404)
    return Response(dumps(history_graph), mimetype='application/json')

@app.errorhandler(404)
@app.errorhandler(400)
def generic_error_handler(error):
    return dumps({'message':error.description}), error.code

@app.route("/graph_test")
def graph_test():
    return redirect(url_for('hello'))

if __name__ == "__main__":
    app.run(debug=True)
