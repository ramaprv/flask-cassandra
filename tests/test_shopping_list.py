import pytest
import requests
import json


REST_SERVER = 'http://localhost:5000/api'


class TestShoppingList :
    def test_post_shopping_list_with_incomplete_data(self):
        values = {  'item' : 'Milk',
                    'quantity' : 2 }
        # Post the data to the webserver.

        res = requests.post(REST_SERVER + '/shopping_list', data=json.dumps(values))
        assert res.status_code == 400

    def test_post_shopping_list_with_complete_data(self):
        values = {  'user_id' : 1,
                    'item' : 'Milk',
                    'quantity' : 2 }
        # Post the data to the webserver.

        res = requests.post(REST_SERVER + '/shopping_list', data=json.dumps(values))
        assert res.status_code == 201

    def test_get_shopping_list_with_user_id(self):
        res = requests.get(REST_SERVER + '/shopping_list/{}'.format(1))
        assert res.status_code == 200

    def test_get_shopping_list_without_user_id(self):
        res = requests.get(REST_SERVER + '/shopping_list/')
        assert res.status_code == 404
