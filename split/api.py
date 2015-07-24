"""
API for querying information about Split courses.
Course information is queried directly from the Split MongoDB collections.
"""

import datetime
import pytz
from bson import ObjectId
from collections import Counter
from mongo import get_collection
from opaque_keys.edx.keys import CourseKey


"""
Raised when course is not found.
"""
class CourseNotFound(Exception):
    pass

"""
Raised when rolling back a course branch to a version not in the course branch's history.
"""
class VersionNotInHistory(Exception):
    pass

"""
Raised when a course rollback fails.
"""
class RollbackFailed(Exception):
    pass


def get_courses():
    """
    Returns a list of CourseKeys for all Split courses from MongoDB.
    """
    coll = get_collection('modulestore.active_versions')
    courses = []
    for course in coll.find():
        courses.append(course)
    return courses

def _get_active_versions(course_key):
    """
    Get the active versions document for a course.
    """
    coll = get_collection('modulestore.active_versions')
    return coll.find_one({
        'org': course_key.org,
        'course': course_key.course,
        'run': course_key.run,
    })

def get_structure_by_key(course_key):
    """
    Returns structure id of current structure for a course branch.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    branch = course_key.branch or 'published-branch'
    coll = get_collection('modulestore.active_versions')
    course = coll.find_one({
        'org': course_key.org,
        'course': course_key.course,
        'run': course_key.run,
    })
    if course is None:
        raise CourseNotFound
    else:
        return course['versions'][branch]

def get_structure_id(course_key):
    """
    Returns structure id of current structure for a course branch.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    branch = course_key.branch or 'published-branch'
    course = _get_active_versions(course_key)
    if course is None:
        raise CourseNotFound
    else:
        return course['versions'][branch]

def get_structure(struct_id):
    """
    Return the entire course structure as a dict.
    """
    coll = get_collection('modulestore.structures')
    return coll.find_one({'_id' : ObjectId(struct_id)})

def get_structure_history(course_key):
    """
    Returns a ordered list of structure ids, starting with original and ending with the newest structure id.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    history = []
    branch = course_key.branch or 'published-branch'
    struct_id = get_structure_id(course_key.for_branch(branch))
    while struct_id:
        history.insert(0, str(struct_id))
        struct_id = get_structure(struct_id)['previous_version']
    return history

def get_structure_history_graph(course_key):
    """
    Returns a complete structure history graph for a course, including any dead branches.
    The return format is:
    Root structure id, {struct_id1: [child_struct_id1, child_struct_id2], struct_id2: [child_struct_id3], etc...}
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    branch = course_key.branch or 'published-branch'
    history = get_structure_history(course_key.for_branch(branch))
    # Now iterate through the history and find all structures which claim each
    # structure as its previous version.
    coll = get_collection('modulestore.structures')
    graph = {'root':[str(history[0])]}
    for struct_id in history:
        all_children = coll.find({'previous_version': ObjectId(struct_id)}, projection=['_id'])
        graph[str(struct_id)] = [str(c['_id']) for c in all_children]
    return graph

def get_course_metadata(course_key):
    """
    Returns a dict of course_module field data.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    """
    return {}

def get_block_counts(struct_id):
    """
    Returns a dict of block_type and the number of each block type in a particular course structure.
    """
    struct = get_structure(struct_id)
    block_counts = Counter()
    for block in struct['blocks']:
        block_counts.update({block['block_type']: 1})
    return dict(block_counts)

def rollback_to_structure_id(course_key, struct_id, verify_in_history=True):
    """
    Rollback a course to a previous structure version.
    Optionally verify that the structure is actually in the course's version history.
    Returns the new active_versions document.
    If no course branch is specified in the course_key, published-branch is assumed.
    If no course is found, raises CourseNotFound.
    If a history check is made and fails, raises VersionNotInHistory.
    If the update fails, raises RollbackFailed.
    """
    branch = course_key.branch or 'published-branch'
    if verify_in_history:
        history = get_structure_history(course_key.for_branch(branch))
        if struct_id not in history:
            raise VersionNotInHistory

    # Grab the current active version (and verify that the course exists).
    course_index = _get_active_versions(course_key)

    # Change the course's active version.
    course_index['versions'][branch] = struct_id
    course_index['last_update'] = datetime.datetime.now(pytz.utc)
    coll = get_collection('modulestore.active_versions')
    result = coll.update({'_id': course_index['_id']}, course_index, upsert=False)
    if result['nModified'] < 1:
        raise RollbackFailed("active_versions update failed.")
    return _get_active_versions(course_key)
