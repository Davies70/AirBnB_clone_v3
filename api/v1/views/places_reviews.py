#!/usr/bin/python3
'''Returns Review details'''

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def all_cities(place_id):
    '''Returns a dict containing all the reviews'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    review_list = []
    for review in reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    '''Gets a review'''
    review = storage.get(Review, id=review_id)
    if review is not None:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    '''Deletes a review'''
    review = storage.get(Review, review_id)
    if review is not None:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    '''Creates a review'''
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    review_data = request.get_json(silent=True)
    if review_data is None:
        abort(400, description='Not a JSON')
    if 'text' not in review_data:
        abort(400, description='Missing text')
    if 'user_id' not in review_data:
        abort(400, description='Missing user_id')

    user = storage.get(User, review_data['user_id'])
    if user is None:
        abort(404)

    review_data.update({'place_id': place_id})
    review = Review(**review_data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    '''Updates a review'''
    review = storage.get(Review, review_id)
    new_data = request.get_json(silent=True)

    if new_data is None:
        abort(400, description='Not a JSON')

    if review is not None:
        old_data = review.to_dict()
        new_data.pop('id', None)
        new_data.pop('place_id', None)
        new_data.pop('user_id', None)
        new_data.pop('created_at', None)
        new_data.pop('updated_at', None)
        old_data.update(new_data)
        updated_review = Review(**old_data)
        updated_review.save()
        return make_response(jsonify(updated_review.to_dict()), 200)
    else:
        abort(404)
