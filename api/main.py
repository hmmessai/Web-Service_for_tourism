import os
import models
from models.city import City
from models.place import Place
from models.user import User
from flask import (
    Blueprint, request, render_template, redirect, url_for, session
)
from flask import (
    current_app, send_from_directory
)
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    citys = models.storage.all('City')
    cities = []
    try:
        for v in citys.values():
            cities.append(v.to_dict())

        sorted_cities = sorted(cities, key=lambda kv: kv['name'])
    except Exception:
        sorted_cities = []

    return render_template('main.html', cities=sorted_cities)

@bp.route('/contribute')
def contribute():
    citys = models.storage.all('City')
    cities = []
    for v in citys.values():
        cities.append(v.to_dict())

    sorted_cities = sorted(cities, key=lambda kv: kv['name'])
    return render_template('contribute.html', url=request.url, cities=sorted_cities)

@bp.route('/add-city', methods=['GET', 'POST'])
def addCity():
    if request.method == 'POST':
        name = request.form['name']
        population = request.form['population']
        region = request.form['region']
        weather = request.form['weather']

        data = {
            'name': name,
            'population': population,
            'region': region,
            'weather': weather,
            'created_by': session['user_id']
        }

        city = City(**data)

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{city.id}.jpg")
                image.save(image_path)

        models.storage.new(city)
        models.storage.save()

        return redirect('/')


@bp.route('/add-place', methods=['GET', 'POST'])
def addPlace():
    if request.method == 'POST':
        name = request.form['name']
        cities_id = request.form['cities_id']
        type = request.form['type']
        price = request.form['price']
        address = request.form['address']
        details = request.form['details']

        data = {
            'name': name,
            'city_id': cities_id,
            'type': type,
            'price': price,
            'address': address,
            'details': details
        }

        place = Place(**data)
        models.storage.new(place)
        models.storage.save()

        return redirect(url_for('main.index', _external=True))

@bp.route('/city/<city>')
def city(city):
    citys = models.storage.all('City')
    cities = []

    city = City.get(city)

    places = city.places
    for v in citys.values():
        cities.append(v.to_dict())

    sorted_cities = sorted(cities, key=lambda kv: kv['name'])

    return render_template('city.html', city=city, url=request.url, cities=sorted_cities, places=places)

@bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/update-city/<id>', methods=['GET', 'POST'])
def update_city(id):
    if request.method == 'POST':
        city = City.get(id)
        print(city)
        for k, v in request.form.items():
            setattr(city, k, v)
        city.save()

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{city.id}.jpg")
                image.save(image_path)
        return redirect(url_for('main.city', city=city.id))