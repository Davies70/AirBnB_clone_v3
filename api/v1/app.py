#!/usr/bin/python3
""" Calls the instance of Blueprint and runs the Flask app"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv


HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = int(getenv('HBNB_API_PORT'))
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    ''' close app after each session '''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    ''' handle page not found error '''
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
