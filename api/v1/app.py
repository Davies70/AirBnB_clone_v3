#!/usr/bin/python3
''' Flask app '''
from flask import Flask
from os import getenv
from api.v1.views import app_views
from models import storage


HBNB_API_HOST = getenv('HBNB_API_HOST')
HBNB_API_PORT = int(getenv('HBNB_API_PORT'))
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    ''' close app after each session '''
    storage.close()


if __name__ == '__main__':
    host = '0.0.0.0' if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
    app.run(host=host, port=port, threaded=True)
