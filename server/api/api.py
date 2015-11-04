#!/usr/bin/python

from flask import Flask, request, session, g
from functools import wraps
from helpers import env_constants

import db,logic

####################################################################################################
#                                                                                                  #
#                                          DECORATORS                                              #
#                                                                                                  #
####################################################################################################
class public(object):
    def __init__(self, setup_session = False):
        self.setup_session = setup_session

    def __call__(self, f):
        @wraps(f)
        def decorated_function(*args, **kwds):
            result = f(*args,**kwds)
            if result and result['success'] and self.setup_session:
                session['user_id'] = result.get('user_id')
            return result
        return decorated_function

class loggedin(object):
    def __init__(self, f):
        self.f = f
        
    def __call__(self, *args):
        if session.get('user_id') is None:
            return {'success': False, 'error': env_constants.NOT_LOGGED_IN_ERROR, 'should_logout': True}
        return self.f(*args)

####################################################################################################
#                                                                                                  #
#                                         PUBLIC API                                               #
#                                                                                                  #
####################################################################################################
@public()
def signup():
    # for now user_name, display_name, email, password are required
    if not request.args.get('user_name') or not request.args.get('display_name') or not request.args.get('email') or not request.args.get('password'):
        return {'success': False, 'error': env_constants.INVALID_REQUEST_ERROR}
    
    user_name = request.args.get('user_name')
    display_name = request.args.get('display_name')
    email = request.args.get('email')
    password = request.args.get('password')
    user,error = logic.signup(user_name,display_name,email,password)
    if error:
        return {'success': False, 'error': error}
    session['user_id'] = user_info['user_id']
    return {'success': True, 'my_info':user}

@public()
def login():
    if (not request.args.get('user_name') and not request.args.get('email')) or not request.args.get('password'):
        return {'success': False, 'error': env_constants.INVALID_REQUEST_ERROR}
    user_name = None
    email = None
    password = request.args.get('password')
    if request.args.get('user_name'):
        user_name = request.args.get('user_name')
        if not request.args.get('email'):
            email = user_name
    if request.args.get('email'):
        email = request.args.get('email')
        if not user_name:
            user_name = email
    user_info, error = logic.login(user_name,email,password)
    if error:
        return {'success': False, 'error': error}
    session['user_id'] = user_info['user_id']
    return {'success':True, 'my_info':user_info}
        
####################################################################################################
#                                                                                                  #
#                                      LOGGED IN API                                               #
#                                                                                                  #
####################################################################################################
@loggedin
def get_user():
    user_id = request.args.get('user_id')
    if not user_id:
        return {'success':False,'error':env_constants.INVALID_REQUEST_ERROR}
    
    user = logic.get_user(user_id)
    if not user:
        return {'success':False,'error':'No such user exists'}
    return {'success':True, 'user':user}

@loggedin
def create_thread():
    if not request.args.get('user_id'):
        return {'success': False, 'error': env_constants.INVALID_REQUEST_ERROR}
    user_id = request.args.get('user_id')
    new_thread, error = logic.create_thread(user_id)
    if error:
        return {'success': False, 'error': error}
    return {'success': True, 'thread':new_thread}

@loggedin
def send_message():
    if not request.args.get('user_id') or not request.args.get('thread_id') or (not request.args.get('message_text') and not request.args.get('message_pic')):
        return {'success': False, 'error': env_constants.INVALID_REQUEST_ERROR}
    user_id = request.args.get('user_id')
    thread_id = request.args.get('thread_id')
    message_text = request.args.get('message_text')
    message_pic = request.args.get('message_pic')
    new_message, error = logic.send_message(user_id,thread_id,message_text,message_pic)
    if error:
        return {'success': False, 'error':error}
    return {'success': True, 'message':new_message}

@loggedin
def get_thread():
    thread_id = request.args.get('thread_id')
    if not thread_id or thread_id < 0:
        return {'success': False, 'error': env_constants.INVALID_REQUEST_ERROR}
    thread = logic.get_thread(thread_id,messages=True)
    return {'success': True, 'thread': thread}

@loggedin
def get_later_messages():
    thread_id = request.args.get('thread_id')
    last_message_id = request.args.get('last_message_id')
    user_id = session.get('user_id')
    if not thread_id or not last_message_id or thread_id < 0 or last_message_id < 0:
        return {'success': False, 'error': env_constants.INVALID_REQUEST_ERROR}
    messages, error = logic.get_later_messages(thread_id=thread_id, last_message_id=last_message_id, user_id=user_id)
    if error:
        return {'success': False, 'error': error}
    return {'success': True, 'messages': messages}

@loggedin
def logout():
    session.clear()
    return {'success':True}
