import pytest
import requests
import json


REST_SERVER = 'http://localhost:5000'


class TestShoppingList :
    def test_post_shopping_list_with_incomplete_data(self):
        values = {  'item' : 'Milk',
                    'quantity' : 2 }
        # Post the data to the webserver.

        res = requests.post(REST_SERVER + '/shopping_list', data=json.dumps(values))
        assert res.status_code == 200

    def test_post_shopping_list_with_complete_data(self):
        values = {  'user_id' : 1,
                    'item' : 'Milk',
                    'quantity' : 2 }
        # Post the data to the webserver.

        res = requests.post(REST_SERVER + '/shopping_list', data=json.dumps(values))
        assert res.status_code == 200

    def test_get_shopping_list_with_user_id(self):
        res = requests.get(REST_SERVER + '/shopping_list/{}'.format(1))
        assert res.status_code == 200

    def test_get_shopping_list_without_user_id(self):
        res = requests.get(REST_SERVER + '/shopping_list/')
        assert res.status_code == 404

    def test_update_shopping_list_with_invalid_id(self):
        res = requests.put(REST_SERVER + '/shopping_list/abcd')
        assert res.status_code == 200

    def test_delete_shopping_list_with_invalid_id(self):
        res = requests.delete(url, **kwargs)(REST_SERVER + '/shopping_list/abcd')
        assert res.status_code == 200
