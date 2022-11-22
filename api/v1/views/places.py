#!/usr/bin/python3
'''Returns Place details'''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def all_cities(city_id):
    '''Returns a dict containing all the places'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    place_list = []
    for place in places:
        place_list.append(place.to_dict())
    return jsonify(place_list)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    '''Gets a place'''
    place = storage.get(Place, id=place_id)
    if place is not None:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Deletes a place'''
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    '''Creates a place'''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    place_data = request.get_json(silent=True)
    if place_data is None:
        abort(400, description='Not a JSON')
    if 'name' not in place_data:
        abort(400, description='Missing name')
    if 'user_id' not in place_data:
        abort(400, description='Missing user_id')

    user = storage.get(User, place_data['user_id'])
    if user is None:
        abort(404)

    place_data.update({'city_id': city_id})
    place = Place(**place_data)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    '''Updates a place'''
    place = storage.get(Place, place_id)
    new_data = request.get_json(silent=True)

    if new_data is None:
        abort(400, description='Not a JSON')

    if place is not None:
        old_data = place.to_dict()
        new_data.pop('id', None)
        new_data.pop('city_id', None)
        new_data.pop('user_id', None)
        new_data.pop('created_at', None)
        new_data.pop('updated_at', None)
        old_data.update(new_data)
        updated_place = Place(**old_data)
        updated_place.save()
        return make_response(jsonify(updated_place.to_dict()), 200)
    else:
        abort(404)
