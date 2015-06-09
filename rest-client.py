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
     values = { 'user_id' : user_id,
                'item' : item,
                'quantity' : quantity }
    # Post the data to the webserver.
    res = requests.post(REST_SERVER + '/shopping_list', data=values)
    return json.loads(res.text)


def fetch_data():
    """
    Fetch data from the REST server.
    """
    user_id = raw_input("user id: ")

    res = requests.get(REST_SERVER + '/shopping_list/'+user_id)
    return json.loads(res.text)


def main(argv=None):
    if argv[1] == 'post':
        data = post_data()
        print json.dumps(data,
                         sort_keys=True,
                         indent=2,
                         separators=(',',':'))
    elif argv[1] == 'fetch':
        data = fetch_data()
        print json.dumps(data,
                         sort_keys=True,
                         indent=2,
                         separators=(',',':'))

if __name__ == '__main__':
    # So that we don't get so many random warnings.
    requests_log = logging.getLogger("requests")
    requests_log.setLevel(logging.WARNING)

    main(sys.argv)
