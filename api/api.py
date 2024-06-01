import models
from models.city import City
from models.place import Place

from flask import (
    Blueprint, request,
)

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/all')
def all():
    all_obj = models.storage.all()

    all_dict ={}
    for k, v in all_obj.items():
        all_dict[k] = v.to_dict()
    return all_dict

@bp.route('/place')
def place():
    places = models.storage.all('Place')

    places_dict ={}
    for k, v in places.items():
        places_dict[k] = v.to_dict()
    return places_dict

@bp.route('/city')
def city():
    cities = models.storage.all('City')

    cities_dict ={}
    for k, v in cities.items():
        cities_dict[k] = v.to_dict()
    return cities_dict

@bp.route('/create-city', methods=['GET', 'POST'])
def create_city():
    name = request.form['name']
    city = City(name=name)
    city.save()
    return city.to_dict()

@bp.route('/create-place', methods=['GET', 'POST'])
def create_place():
    name = request.form['name']
    place = Place(name=name)
    place.save()
    return place.to_dict()

@bp.route('/search-cities', methods=['GET', 'POST'])
def search_cities():
    key = request.json
    keyword = key.get('keyword')
    cities_list = []

    results = models.storage.search("City", keyword)

    for i in results:
        cities_list.append(i.to_dict())

    return cities_list