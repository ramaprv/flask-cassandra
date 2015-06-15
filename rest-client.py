import json
import logging
import requests
import sys


REST_SERVER = 'http://localhost:5000'

def signup_data():
    """
    Post new user to the REST server.
    """

    handle = raw_input("handle : ")
    password = raw_input("password : ")
    phone = raw_input("phone : ")
    values = {  'handle' : str(handle),
                'password' : str(password),
                'phone' : int(phone) }
    # Post the data to the webserver.
    print values
    res = requests.post(REST_SERVER + '/api/signup', data=json.dumps(values))
    if res.status_code == 201:
        return(res.text)
    else:
        return (res.status_code)


def login_data():
    """
    User login to the REST server.
    """

    handle = raw_input("handle : ")
    password = raw_input("password : ")
    values = {  'handle' : str(handle),
                'password' : str(password) }
    # Post the data to the webserver.
    print values
    res = requests.post(REST_SERVER + '/api/login', data=json.dumps(values))
    if res.status_code == 202:
        return(res.text)
    else:
        return (res.status_code)

def logout_data():
    """
    User logout off the REST server.
    """

    res = requests.get(REST_SERVER + '/api/logout')
    if res.status_code == 202:
        return(res.text)
    else:
        return (res.status_code)


def check_login_data():
    """
    User Login Check the REST server.
    """

    res = requests.get(REST_SERVER + '/api/')
    if res.status_code == 200:
        return(res.text)
    else:
        return (res.status_code)


def post_data():
    """
    Post some data to the REST server.
    """

    user_id = raw_input("user_id : ")
    item = raw_input("item : ")
    quantity = raw_input("quantity : ")
    values = {  'user_id' : int(user_id),
                'item' : item,
                'quantity' : int(quantity) }
    # Post the data to the webserver.
    print values
    res = requests.post(REST_SERVER + '/api/shopping_list', data=json.dumps(values))
    if res.status_code == 201:
        return(res.text)
    else:
        return (res.status_code)


def fetch_data():
    """
    Fetch data from the REST server.
    """
    user_id = raw_input("user id: ")

    res = requests.get(REST_SERVER + '/api/shopping_list/{}'.format(user_id))
    if res.status_code == 200:
        return(res.text)
    else:
        return (res.status_code)


def update_data():
    """
    Update data to the REST server.
    """
    shopping_list_id = raw_input("shopping list id: ")
    item = raw_input("item : ")
    quantity = raw_input("quantity : ")
    values = {  'item' : item,
                'quantity' : int(quantity) }

    res = requests.put(REST_SERVER + '/shopping_list/{}'.format(shopping_list_id), data=json.dumps(values))
    if res.status_code == 205:
        return(res.text)
    else:
        return (res.status_code)


def delete_data():
    """
    Delete data from the REST server.
    """
    shopping_list_id = raw_input("shopping list id: ")

    res = requests.delete(REST_SERVER + '/api/shopping_list/{}'.format(shopping_list_id))
    if res.status_code == 204:
        return(res.text)
    else:
        return (res.status_code)


def main(argv=None):
    if argv[1] == 'post':
        data = post_data()
        print data
    elif argv[1] == 'fetch':
        data = fetch_data()
        print data
    elif argv[1] == 'update':
        data = update_data()
        print data
    elif argv[1] == 'delete':
        data = delete_data()
        print data
    elif argv[1] == 'signup':
        data = signup_data()
        print data
    elif argv[1] == 'login':
        data = login_data()
        print data
    elif argv[1] == 'logout':
        data = logout_data()
        print data
    elif argv[1] == 'check':
        data = check_login_data()
        print data

if __name__ == '__main__':
    # So that we don't get so many random warnings.
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    main(sys.argv)
