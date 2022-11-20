#!/usr/bin/python3
''' Flask app '''
from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv


host = getenv('HBNB_API_HOST')
port = int(getenv('HBNB_API_PORT'))
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exception):
    ''' close app after each session '''
    storage.close()


if __name__ == '__main__':
    app.run(host=host, port=port, threaded=True)
