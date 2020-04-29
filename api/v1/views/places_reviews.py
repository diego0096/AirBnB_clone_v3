#!/usr/bin/python3
""" View for State objects to make API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """ Retrieves the list of all objects """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)

    if request.method == 'GET':
        review_list = []
        for review in place_obj.reviews:
            review_list.append(review.to_dict())
        return jsonify(review_list)

    if request.method == 'POST':
        review_request = request.get_json()
        if review_request is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'user_id' not in review_request:
            return make_response(jsonify({'error': 'Missing user_id'}), 400)
        user_name = storage.get("User", review_request['user_id'])
        if not user_name:
            abort(404)
        if 'text' not in review_request:
            return make_response(jsonify({'error': 'Missing text'}), 400)
        review_request['place_id'] = place_id
        review = Review(**review_request)
        review.save()
        return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def get_review(review_id):
    '''Get a review given a review_id'''
    review_obj = storage.get("Place", review_id)
    if review_obj is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review_obj.to_dict())

    if request.method == 'DELETE':
        review_obj.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        review_request = request.get_json()
        if review_request is None:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, value in review_request.items():
            if attr not in ['id', 'user_id', 'updated_at', 'place_id',
                            'created_at']:
                setattr(review_obj, attr, value)
        review_obj.save()
        return jsonify(review_obj.to_dict())
