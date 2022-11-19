#!/usr/bin/python3
''' Use Blueprint instance '''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def return_status():
    ''' returns status code'''
    return jsonify({"status": "OK"})
