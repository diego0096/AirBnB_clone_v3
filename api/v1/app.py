#!/usr/bin/python3
'''Starts a web application for API connection'''
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
import os


app = Flask(__name__)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)


@app.teardown_appcontext
def app_context(close):
    '''calls storage.close(). It is called after each request'''
    storage.close()


@app.errorhandler(404)
def not_found(error):
    '''Returns a JSON-formatted 404 status code response'''
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":
    '''flask run from this file'''
    app.run(host=host, port=port, threaded=True)
