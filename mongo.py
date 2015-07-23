"""
Utility functions for connecting to Mongo.
"""

import os
import pymongo
import logging


log = logging.getLogger(__name__)

# Use this connection info unless overridden.
DEFAULT_CONN_INFO = {
    'host': 'localhost',
    'port': 27017,
    'dbname': 'edxapp',
    'user': 'edxapp',
    'password': None,
}

# Name of Split structures collection.
SPLIT_STRUCTURES_COLLECTION = 'modulestore.structures'


def structures_collection():
    """
    Returns a PyMongo Collection object for Split structures.
    """
    # Override Mongo server/credentials using environment variables.
    mongo_conn_info = {}
    for env_var, name in (
        (SPLIT_UTILS_HOST, 'host'),
        (SPLIT_UTILS_PORT, 'port'),
        (SPLIT_UTILS_DB, 'dbname'),
        (SPLIT_UTILS_USERNAME, 'user'),
        (SPLIT_UTILS_PASSWORD, 'password'),
    ):
        mongo_conn_info[name] = os.getenv(env_var, DEFAULT_CONN_INFO[name])

    # Connect to Mongo database.
    client = pymongo.MongoClient(
        host=mongo_conn_info['host'],
        port=mongo_conn_info['port'],
    )
    try:
        db = client[mongo_conn_info['dbname']]
    except InvalidName:
        log.critical("Mongo instance at {}:{} has no '{}' database".format(
            mongo_conn_info['host'],
            mongo_conn_info['port'],
            mongo_conn_info['dbname']
        ))
        return None

    db.authenticate(mongo_conn_info['username'], mongo_conn_info['password'])

    try:
        structures_coll = pymongo.collection.Collection(
            db,
            SPLIT_STRUCTURES_COLLECTION
        )
    except InvalidName:
        log.critical("Mongo instance at {}:{} has no '{}' collection in the {}' database".format(
            mongo_conn_info['host'],
            mongo_conn_info['port'],
            SPLIT_STRUCTURES_COLLECTION,
            mongo_conn_info['dbname']
        ))
        return None

    return structures_coll
