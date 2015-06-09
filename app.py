import datetime
import json
import os
import time_uuid
import uuid
from cassandra.cluster import Cluster
from flask import Flask, request

def _connect_to_cassandra(keyspace):
    """
    Connect to the Cassandra cluster and return the session.
    """

    if 'CASSANDRA_URL' in os.environ:
        host = os.environ['CASSANDRA_URL']
    else:
        host = 'localhost'

    cluster = Cluster([host])
    session = cluster.connect(keyspace)

    return session

"""
Create the Flask application, connect to Cassandra, and then
set up all the routes.
"""
app = Flask(__name__)
session = _connect_to_cassandra('shop')

@app.route('/shopping_list/<user_id>', methods=['GET'])
def get_shopping_list(user_id):
    """
    Fetch shopping_list
    """

    user_id = str(request.args['user_id'])


    query = """SELECT * FROM shopping_list
               WHERE user_id=%(user_id)s
               ORDER BY created_at DESC"""

    values = { 'user_id': user_id }

    rows = session.execute(query, values)
    reply = { 'results' : [] }
    for r in rows:
        ts = time_uuid.TimeUUID(str(r.time))
        dt = str(ts.get_datetime())
        reply['results'].append({ 'item' : str(r.item),
                                  'quantity': str(r.quantity),
                                  'created_at': str(created_at) })
    return json.dumps(reply)

@app.route('/shopping_list', methods=['POST'])
def put_shopping_list():
    """
    Insert shopping_list
    """

    user_id = str(request.args['user_id'])
    item = str(request.args['item'])
    quantity = float(request.args['quantity'])

    day = datetime.datetime.utcnow() - datetime.timedelta(days=days)
    timestamp = time_uuid.TimeUUID.with_utc(day, randomize=False, lowest_val=True)

    query = """INSERT INTO shopping_list
               (user_id, created_at, item, quantity)
               VALUES (%(user_id)s, %(created_at)s, %(item)s, %(quantitiy)f)"""

    values = { 'user_id': user_id,
               'created_at': timestamp,
               'item': item,
               'quantity': quantity }

    session.execute(query, values)

    reply = { 'result' : values }
    return json.dumps(reply)

if __name__ == '__main__':
    app.run()
