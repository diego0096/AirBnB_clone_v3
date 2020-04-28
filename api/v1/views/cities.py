#!/usr/bin/python3
'''View for City objects that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id=None):
    '''Return list of all City objects of a State

    state_obj: Is a state object taht belongs to the state_id.'''

    state_obj = storage.get("State", state_id)
    if state_obj is None:
        return abort(404, description="Not found")

    all_cities = storage.all("City").values()
    cities = []
    for city in all_cities:
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)
