#!/usr/bin/python

from helpers import env_constants
from flask import Flask, request, jsonify
from api import api

import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return "<span style='color:red'>I am app 1</span>"

@app.route('/api/<api_func>')
def api_call(api_func):
    if not api_func:
        response = {'success':False, 'error':'No such api call exists'}
        return jsonify(**response)
    try:
        try:
            func = getattr(api, str(api_func))
        except AttributeError:
            response = {'success':False, 'error':env_constants.NO_SUCH_API_ERROR}
        else:
            response = func()
        if not response:
            response = {'success':True, 'no_return': True}
        if isinstance(response,dict):
            return jsonify(**response)
        else:
            return response
    except Exception,e:
        return traceback.print_exc()
        return "Some error occurred %r" % e

'''@app.errorhandler(404)
def page_not_found(error):
    return flask.jsonify({'success':False, 'error':'No such api call exists'})'''

@app.errorhandler(500)
def internal_error(error):
    return error

if __name__ == "__main__":
    app.secret_key = "WishIKnewWhatTheSECRETWasForJugaado"
    app.run('0.0.0.0', 8080, debug=True)
