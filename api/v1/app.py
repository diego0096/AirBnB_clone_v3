#!/usr/bin/python3
'''API connection'''
from flask import Flask, Blueprint
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def app_context(close):
    '''calls storage.close()'''
    storage.close()


if __name__ == "__main__":
    '''flask run from this file'''
    app.run(host="0.0.0.0", port=5000, threaded=True)
