#!/usr/bin/python3
'''Get status/'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
classes = {"users": "User", "places": "Place",
            "states": "State", "cities": "City",
            "amenities": "Amenity", "reviews": "Review"}

@app_views.route('/status')
def status():
    '''Return status (json format) of the object app_views'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats')
def stats():
    """ Returns the number of each instance type """
    # return jsonify(amenities=storage.count("Amenity"),
    #                cities=storage.count("City"),
    #                places=storage.count("Place"),
    #                reviews=storage.count("Review"),
    #                states=storage.count("State"),
    #                users=storage.count("User"))
    instance_count = {}
    for key, value in classes.items():
        instance_count[key] = storage.count(value)
    return jsonify(instance_count)
