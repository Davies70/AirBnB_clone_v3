#!/usr/bin/python3
'''view for Place objects that handles all default RESTFul API actions'''

from api.v1.views import app_views
from models import storage
from flask import abort, jsonify, make_response, request
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def place_by_city(city_id):
    ''' get and post place object '''
    if request.method == 'GET':
        city_obj = storage.get(City, city_id)
        place_list = []
        if city_obj is None:
            abort(404)
        place_obj = getattr(city_obj, 'places')
        for place in place_obj:
            place_list.append(place.to_dict())
        return jsonify(place_list)

    if request.method == 'POST':
        city_obj = storage.get(City, city_id)
        if city_obj is None:
            abort(404)
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.get_json()
            if 'user_id' not in body:
                abort(400, description='Missing user_id')
            user_id = body.get('user_id')
            user_obj = storage.get(User, user_id)
            if user_obj is None:
                abort(404)
            if 'name' not in body:
                abort(400, description='Missing name')
            new_place = Place(**body)
            setattr(new_place, 'city_id', city_id)
            storage.new(new_place)
            storage.save()
            return make_response(jsonify(new_place.to_dict()), 201)
        else:
            abort(400, description='Not a JSON')


@app_views.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def place_by_id(place_id):
    ''' get, delete, and put place objects '''
    if request.method == 'GET':
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        return jsonify(place_obj.to_dict())

    if request.method == 'DELETE':
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        storage.delete(place_obj)
        storage.save()
        return make_response({}, 200)

    if request.method == 'PUT':
        place_obj = storage.get(Place, place_id)
        if place_obj is None:
            abort(404)
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            body = request.get_json()
            banned_keys = ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']
            for key, value in body.items():
                if key not in banned_keys:
                    setattr(place_obj, key, value)
            storage.save()
            return make_response(jsonify(place_obj.to_dict()), 200)
        else:
            abort(400, description='Not a JSON')
