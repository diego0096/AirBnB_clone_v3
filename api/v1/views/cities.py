#!/usr/bin/python3
'''View for City objects that handles all default RestFul API actions'''
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_cities(state_id=None):
    '''GET: Return json list of all City objects of a State
       POST: Create a new city object for a state with a given state_id

    - state_obj: Is a state object taht belongs to the state_id.
    - state_id: id of the state. If it does not exist, return None
    - all_cities: list of all cities objects with their attributes
    - cities: list to jsonify. Is the return of this method'''

    state_obj = storage.get("State", state_id)
    if state_obj is None:
        return abort(404, description="Not found")

    if request.method == 'GET':
        all_cities = storage.all("City").values()
        cities = []
        for city in all_cities:
            if city.state_id == state_id:
                cities.append(city.to_dict())
        return jsonify(cities)

    elif request.method == 'POST':
        city_request = request.get_json()
        if city_request is None:
            abort(400, "Not a JSON")
        if city_request.get("name") is None:
            abort(400, "Missing name")
        # column new_city can't be Null, so we add an id
        city_request['state_id'] = state_id
        new_city = City(**city_request)
        storage.new(new_city)
        storage.save()
        return make_response(jsonify(new_city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE'])
def get_or_delete_city(city_id):
    '''GET: Return json City object that belongs to the given city_id
       DELETE: Delete a city object that belongs to the given city id'''
    city_obj = storage.get("City", city_id)
    if city_obj is None:
        return abort(404, description="Not found")

    if request.method == 'GET':
        all_cities = storage.all("City").values()
        for city in all_cities:
            if city.id == city_id:
                return jsonify(city.to_dict())
    elif request.method == 'DELETE':
        city_obj.delete()
        storage.save()
        return make_response(jsonify({}), 200)
