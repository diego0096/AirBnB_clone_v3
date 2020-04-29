#!/usr/bin/python3
'''Get status/'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    '''Return status (json format) of the object app_views'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """ Returns the number of each instance type """
    return jsonify(amenities=storage.count("Amenity"),
                   cities=storage.count("City"),
                   places=storage.count("Place"),
                   reviews=storage.count("Review"),
                   states=storage.count("State"),
                   users=storage.count("User"))
