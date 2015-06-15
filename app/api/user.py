import json

from flask import (Flask, session, redirect, url_for, escape, request,
    make_response, jsonify)
from werkzeug.security import generate_password_hash, \
     check_password_hash
from app.api import api
from app.models import User


def hash_password(password):
    return generate_password_hash(password)

def check_password(hash_password, password):
    return check_password_hash(hash_password, password)

@api.route('/', methods=['GET'])
def index():
    if 'handle' in session:
        return make_response(jsonify(({'success':False,
            'result':'Logged in as {}'}).format(escape(session['handle']))), 200)
    return make_response(jsonify({'success':False,
        'result':'Not Logged in'}), 401)


@api.route('/signup', methods=['POST'])
def signup():
    data = json.loads(request.data)

    if 'handle' in data and 'password' in data:
        handle = str(data['handle'])
        password = hash_password(str(data['password']))
        if 'email' in data:
            email = ''.join(str(e) for e in data['email'])
            User.create(handle=handle, email=email, password=password)
            return make_response(jsonify({'success':True,'result':
                'Signup Successful for {}'.format(handle)}), 201)
        elif 'phone' in data:
            phone = int(data['phone'])
            User.create(handle=handle, phone=phone, password=password)
            return make_response(jsonify({'success':True,'result':
                'Signup Successful for {}'.format(handle)}), 201)
    else:
        return make_response(jsonify({'success':False,'result':'Incomplete parameters'}), 400)


@api.route('/login', methods=['POST'])
def login():
    data = json.loads(request.data)

    if 'handle' in data and 'password' in data:
        handle = str(data['handle'])
        user = User.get(handle=handle)
        if check_password(user.password,str(data['password'])) == True:
            session['handle'] = handle
            return make_response(jsonify({'success':True,
            'result':'Login Successful'}), 202)
        else:
            return make_response(jsonify({'success':False,
            'result':'Handle Password combination is wrong'}), 401)

    else:
        return make_response(jsonify({'success':False,'result':'Invalid parameters'}), 400)


@api.route('/logout', methods=['GET'])
def logout():
    session.pop('handle', None)
    return make_response(jsonify({'success':True,
        'result':'Logged out'}), 202)
