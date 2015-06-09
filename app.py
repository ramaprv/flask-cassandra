import json
import os
import time_uuid
import datetime

from uuid import UUID
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


def _validate_uuid4(uuid_string):
    """
    Validate that a UUID string is in
    fact a valid uuid4.
    """

    try:
        val = UUID(uuid_string, version=4)
    except ValueError:
        return False

    return val.hex == uuid_string


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
            data['results'].append({ 'id' : instance.id,
                                     'user_id' : instance.user_id,
                                     'item' : instance.item,
                                     'quantity' : instance.quantity })
            i += 1
            if i == query.count():
                return str(data)
    else:
        return json.dumps({'success':True,'results':'Empty Shopping List'})


@app.route('/shopping_list', methods=['POST'])
def post_shopping_list():
    """
    Insert shopping_list
    """

    data = json.loads(request.data)

    if hasattr(data, 'user_id'):
        user_id = int(data['user_id'])
    else:
        return json.dumps({'success':False,'result':'User id is empty'})

    if hasattr(data, 'item'):
        item = ''.join(str(e) for e in data['item'])
    else:
        return json.dumps({'success':False,'result':'Item is empty'})

    if hasattr(data, 'quantity'):
        quantity = int(data['quantity'])
    else:
        return json.dumps({'success':False,'result':'Quantity is empty'})

    Shopping_List.create(user_id=user_id, item=item, quantity=quantity)

    return json.dumps({'success':True,'result':'Shopping List Updated'})


@app.route('/shopping_list/<id>', methods=['PUT'])
def update_shopping_list(id):
    """
    Update shopping_list
    """

    if _validate_uuid4(id):
        data = json.loads(request.data)
        update_param = ''

        query = Shopping_List.get(id=id)
        if hasattr(data, 'item'):
            item = ''.join(str(e) for e in data['item'])
            query.update(item=item)
        if hasattr(data, 'quantity'):
            quantity = int(data['quantity'])
            query.update(quantity=quantity)
        return json.dumps({'success':True,'result':'Shopping list updated'})
    else:
        return json.dumps({'success':False,'result':'Invalid shopping list id'})


@app.route('/shopping_list/<id>', methods=['DELETE'])
def delete_shopping_list(id):
    """
    Delete shopping_list
    """

    if _validate_uuid4(id):
        query = Shopping_List.get(id=id)
        query.delete()
        return json.dumps({'success':True,'result':'Shopping list deleted'})
    else:
        return json.dumps({'success':False,'result':'Invalid shopping list id'})


if __name__ == '__main__':
    app.run(debug=True)
