"""
API for querying information about Split courses.
Course information is queried directly from the Split MongoDB collections.
"""

from opaque_keys.edx.keys import CourseKey
from mongo import get_collection



def get_courses():
    """
    Returns a list of CourseKeys for all Split courses from MongoDB.
    """
    coll = get_collection('modulestore.active_versions')
    courses = []
    for course in coll.find():
        courses.append((course))
    return courses


def get_structure_id(course_key):
    """
    Returns structure id of current structure for a course branch.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    pass

def get_structure(struct_id):
    """
    Return the entire course structure as a dict.
    """
    pass

def get_structure_history(course_key):
    """
    Returns a ordered list of structure ids, starting with origin and ending with current.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    pass

def get_structure_history_graph(course_key):
    """
    Return a complete structure history graph for a course, including any dead branches.
    The return format is:
    Root structure id, {struct_id1: [child_struct_id1, child_struct_id2], struct_id2: [child_struct_id3], etc...}
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    pass

def get_course_metadata(course_key):
    """
    Returns a dict of course_module field data.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    return {}
