import os
import models
from models.city import City
from models.place import Place
from flask import (
    Blueprint, request, render_template, redirect, url_for
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
    for v in citys.values():
        cities.append(v.to_dict())

    sorted_cities = sorted(cities, key=lambda kv: kv['name'])

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
            'weather': weather
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
        city = request.form['city']
        type = request.form['type']
        price = request.form['price']
        address = request.form['address']
        details = request.form['details']

        data = {
            'name': name,
            'city': city,
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
    places = City.places(city)
    for v in citys.values():
        cities.append(v.to_dict())

    city = City.search(city)
    sorted_cities = sorted(cities, key=lambda kv: kv['name'])

    return render_template('city.html', city=city, url=request.url, cities=sorted_cities, places=places)

@bp.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)


@bp.route('/update-city', methods=['GET', 'POST'])
def update_city():
    if request.method == 'POST':
        city = City.search(request.form['name'])
        for k, v in request.form.items():
            setattr(city, k, v)
        city.save()

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], f"{city.id}.jpg")
                image.save(image_path)
        return redirect(url_for('main.city', city=city.name))