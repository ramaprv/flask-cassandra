import json
import os
import time_uuid
import datetime

from flask import Flask, request
from cqlengine import connection
from cqlengine.management import sync_table
from models import Shopping_List


"""
Create the Flask application, connect to Cassandra, and then
set up all the routes.
"""
app = Flask(__name__)

"""
Connect to the demo keyspace on our cluster running at 127.0.0.1
"""

connection.setup(['127.0.0.1'], "shop")
sync_table(Shopping_List)


@app.route('/shopping_list/<id>', methods=['GET'])
def get_shopping_list(id):
    """
    Fetch shopping_list
    """
    query = Shopping_List.objects(user_id=int(id))
    if query.count > 0:
        data = { 'results' : [] }
        i = 0
        for instance in query:
            data['results'].append(instance)
            i += 1
            if i == query.count():
                return str(data)
    else:
        return json.dumps({'success':False,'results':'Empty Shopping List'})


@app.route('/shopping_list', methods=['POST'])
def post_shopping_list():
    """
    Insert shopping_list
    """

    data = json.loads(request.data)
    user_id = int(data['user_id'])
    item = ''.join(str(e) for e in data['item'])
    quantity = int(data['quantity'])

    Shopping_List.create(user_id=user_id, item=item, quantity=quantity)

    return json.dumps({'success':True})

if __name__ == '__main__':
    app.run(debug=True)
