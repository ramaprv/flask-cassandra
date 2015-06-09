import json
import logging
import requests
import sys


REST_SERVER = 'http://localhost:5000'


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
    res = requests.post(REST_SERVER + '/shopping_list', data=json.dumps(values))
    print(res.status_code, res.reason)
    if res.status_code == 200:
        return(res.text)
    else:
        return (res.status_code)


def fetch_data():
    """
    Fetch data from the REST server.
    """
    user_id = raw_input("user id: ")

    res = requests.get(REST_SERVER + '/shopping_list/{}'.format(user_id))
    print(res.status_code, res.reason)
    if res.status_code == 200:
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
if __name__ == '__main__':
    # So that we don't get so many random warnings.
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    main(sys.argv)
