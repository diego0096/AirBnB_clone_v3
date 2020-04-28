#!/usr/bin/python3
'''View for City objects that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id=None):
    '''Return json list of all City objects of a State

    state_obj: Is a state object taht belongs to the state_id.
    state_id: id of the state. If it does not exist, return None
    all_cities: list of all cities objects with their attributes
    cities: list to jsonify. Is the return of this method'''

    state_obj = storage.get("State", state_id)
    if state_obj is None:
        return abort(404, description="Not found")

    all_cities = storage.all("City").values()
    cities = []
    for city in all_cities:
        if city.state_id == state_id:
            cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'])
def get_or_delete_city(city_id):
    '''GET: Return json City object that belongs to the given city_id'''
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        return abort(404, description="Not found")

    all_cities = storage.all("City"). values()
    for city in all_cities:
        if city.id == city_id:
            return jsonify(city.to_dict())
