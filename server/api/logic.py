#!/usr/bin/python

import db
from helpers import py_helpers, env_constants

def get_user(user_id):
    query = "SELECT * FROM users WHERE user_id = %s LIMIT 1" % user_id
    return db.read_one(query)

def get_thread(thread_id, messages = False):
    query = "SELECT * FROM message_threads WHERE thread_id = %s LIMIT 1" % thread_id
    result = db.read_one(query)
    if messages:
        query = "SELECT * FROM messages WHERE thread_id = %s ORDER BY t_create DESC" % thread_id
        result['messages'] = db.read(query)
    return result

def get_later_messages(thread_id,last_message_id,user_id):
    query = "SELECT * FROM messages WHERE thread_id = %s AND message_id > %s" % (thread_id, last_message_id)
    messages = db.read(query)
    return messages, None

def signup(user_name,display_name,email,password):
    #Check for existing user
    query = "SELECT * FROM users WHERE email = '%s' LIMIT 1" % email
    existing_user = db.read_one(query)
    if existing_user:
        return None, ["This email is already registered with us. If you forgot your password, please reset it.",]
    query = "SELECT * FROM users WHERE user_name = '%s' LIMIT 1" % user_name
    existing_user = db.read_one(query)
    if existing_user:
        return None, ["This user name is not available. Please select a new one"]

    #Okay great! Register now
    password = py_helpers.hash_password(password)
    print "password: " + password
    query = "INSERT INTO users (user_name,display_name,email,password) VALUES('%s','%s','%s','%s')" % (user_name,display_name,email,password)
    new_id = db.write(query)
    if not new_id:
        return None, [env_constants.MYSQL_WRITING_ERROR,]

    query = "SELECT user_id,user_name,display_name,email,t_create,t_update FROM users WHERE user_id = %s LIMIT 1" % new_id
    user_info = db.read_one(query)
    return user_info, None

def login(user_name,email,password):
    query = "SELECT * FROM users WHERE user_name = '%s' OR email = '%s' LIMIT 1" % (user_name,email)
    user_info = db.read_one(query)
    print user_info
    if not user_info:
        return None, ["No such user exists. Get an account now"]
    if not py_helpers.check_password(password, user_info['password']):
        print password
        return None, ["Sorry, password doesn't match. I want to allow you! Trust me. Maybe try FORGOT PASSWORD?"]
    del user_info['password']
    return user_info, None

def create_thread(user_id):
    #First check if user is valid
    user = get_user(user_id)
    if not user:
        return None, ["No such user exists",]
    #query = "SELECT * FROM message_threads WHERE user_id = %s ORDER BY thread_id DESC LIMIT 1" % user_id
    query = "INSERT INTO message_threads (user_id,thread_name) VALUES ('%s','%s')" % (user_id,user['display_name'])
    new_thread_id = db.write(query)
    if not new_thread_id:
        return None, [env_constants.MYSQL_WRITING_ERROR,]
    #query = "SELECT * FROM message_threads WHERE thread_id = %s LIMIT 1" % new_thread_id
    #new_thread = db.read_one(query)
    new_thread = get_thread(new_thread_id)
    return new_thread, None

def send_message(user_id,thread_id,message_text,message_pic):
    user = get_user(user_id)
    if not user:
        return None, ["No such user exists",]
    thread = get_thread(thread_id)
    if not thread:
        return None, ["No such thread exists",]
    if not str(thread['user_id']) == user_id:
        return None, ["Sorry, you don't own this thread",]
    query = "INSERT INTO messages ("
    vals = []
    val_string = ""
    if message_text:
        query = query + "message_text,"
        vals.append(message_text)
        val_string = val_string + "'%s',"
    if message_pic:
        query = query + "message_pic,"
        vals.append(message_pic)
        val_string = val_string + "'%s',"
    query = query + "thread_id,user_id) VALUES(" + val_string + "'%s','%s')"
    vals.append(thread_id)
    vals.append(user_id)
    print query 
    print vals
    query = query % tuple(vals)
    new_message_id = db.write(query)
    if not new_message_id:
        return None, [env_constants.MYSQL_WRITING_ERROR,]
    query = "SELECT * FROM messages WHERE message_id = %s LIMIT 1" % new_message_id
    new_message = db.read_one(query)
    return new_message, None
    

if __name__ == "__main__":
    pass
