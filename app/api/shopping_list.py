import json
import os
import time_uuid
import datetime

from uuid import UUID
from flask import Flask, app, jsonify, abort, request, make_response, url_for
from app.api import api
from app.models import ShoppingList


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

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog


@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)


@api.route('/shopping_list/<id>', methods=['GET'])
def get_shopping_list(id):
    """
    Fetch shopping_list
    """

    query = ShoppingList.objects(user_id=int(id))
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
                return make_response(jsonify(data), 200)
    else:
        return make_response(jsonify({'success':True,'results':'Empty Shopping List'}), 204)


@api.route('/shopping_list', methods=['POST'])
def post_shopping_list():
    """
    Insert shopping_list
    """

    data = json.loads(request.data)

    if hasattr(data, 'user_id'):
        user_id = int(data['user_id'])
    else:
        return make_response(jsonify({'success':False,'result':'User id is empty'}), 400)

    if hasattr(data, 'item'):
        item = ''.join(str(e) for e in data['item'])
    else:
        return make_response(jsonify({'success':False,'result':'Item is empty'}), 400)

    if hasattr(data, 'quantity'):
        quantity = int(data['quantity'])
    else:
        return make_response(jsonify({'success':False,'result':'Quantity is empty'}), 400)

    ShoppingList.create(user_id=user_id, item=item, quantity=quantity)

    return make_response(jsonify({'success':True,'result':'Shopping List Created'}), 201)


@api.route('/shopping_list/<id>', methods=['PUT'])
def update_shopping_list(id):
    """
    Update shopping_list
    """

    if _validate_uuid4(id):
        data = json.loads(request.data)
        update_param = ''

        query = ShoppingList.get(id=id)
        if hasattr(data, 'item'):
            item = ''.join(str(e) for e in data['item'])
            query.update(item=item)
        if hasattr(data, 'quantity'):
            quantity = int(data['quantity'])
            query.update(quantity=quantity)
        return make_response(jsonify({'success':True,'result':'Shopping list updated'}), 201)
    else:
        return make_response(jsonify({'success':False,'result':'Invalid shopping list id'}), 400)


@api.route('/shopping_list/<id>', methods=['DELETE'])
def delete_shopping_list(id):
    """
    Delete shopping_list
    """

    if _validate_uuid4(id):
        query = ShoppingList.get(id=id)
        query.delete()
        return make_response(jsonify({'success':True,'result':'Shopping list deleted'}), 204)
    else:
        return make_response(jsonify({'success':False,'result':'Invalid shopping list id'}), 400)
