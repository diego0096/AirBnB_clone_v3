#!/usr/bin/python3
'''Get status/'''
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    '''Return status (json format) of the object app_views'''
    return jsonify({'status': 'OK'})
