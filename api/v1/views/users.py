#!/usr/bin/python3
""" View for Users objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    '''Retrieves a list of all User objects'''
    list_users = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def r_user_id(user_id):
    """ Retrieves object """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ Deletes an user object """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ Creates an user object """
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "name" not in new_user:
        abort(400, "Missing name")
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """ Updates an object """
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    body_request = request.get_json()
    if not body_request:
        abort(400, "Not a JSON")

    for k, v in body_request.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)