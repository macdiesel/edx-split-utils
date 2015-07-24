"""
Utility functions for connecting to Mongo.
"""

import os
import pymongo
from pymongo.errors import InvalidName
import logging


log = logging.getLogger(__name__)

# Use this connection info unless overridden by environment variables.
DEFAULT_CONN_INFO = {
    'host': 'localhost',
    'port': 27019,
    'dbname': 'edxapp',
    'user': 'edxapp',
    'password': 'password',
}


def get_collection(collection_name):
    """
    Returns a PyMongo Collection object for Split structures.
    """
    # Override Mongo server/credentials using environment variables.
    mongo_conn_info = {}
    for env_var, name in (
        ('SPLIT_UTILS_HOST', 'host'),
        ('SPLIT_UTILS_PORT', 'port'),
        ('SPLIT_UTILS_DB', 'dbname'),
        ('SPLIT_UTILS_USERNAME', 'user'),
        ('SPLIT_UTILS_PASSWORD', 'password'),
    ):
        mongo_conn_info[name] = os.getenv(env_var, DEFAULT_CONN_INFO[name])

    # Connect to Mongo database.
    client = pymongo.MongoClient(
        host=mongo_conn_info['host'],
        port=int(mongo_conn_info['port']),
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

    db.authenticate(mongo_conn_info['user'], mongo_conn_info['password'])

    try:
        collection = pymongo.collection.Collection(
            db,
            collection_name
        )
    except InvalidName:
        log.critical("Mongo instance at {}:{} has no '{}' collection in the {}' database".format(
            mongo_conn_info['host'],
            mongo_conn_info['port'],
            collection_name,
            mongo_conn_info['dbname']
        ))
        return None

    return collection
