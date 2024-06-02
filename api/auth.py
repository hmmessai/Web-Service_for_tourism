import models
import bcrypt
from models.user import User
from models.city import City
from flask import (
    Blueprint, request, render_template, url_for, redirect, make_response, session
)
import MySQLdb
from MySQLdb import IntegrityError
import sqlalchemy

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user_name = request.form.get('name')
        password = request.form.get('password')
        if user_name and password:
            try:
                user = User.search(user_name)
                if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                    response = make_response(redirect(url_for('main.index')))
                    # response.set_cookie('user_id', user.id)
                    session['user_id'] = user.id
                    if checkauth():
                        return response
                    else:
                        error = "Couldn't create session"
                else:
                    error = "Invalid username or password"
            except Exception as e:
                error = str(e)
        else:
            error = "Username and password are required"
    return render_template('login.html', error=error, cities=[])

    
@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    cities = models.storage.all(City)
    if request.method == 'POST':
            try:
                address = request.form['address']
                city_id = request.form['city_id']
                name = request.form['name']
                phone_number = request.form['phone_number']
                password = request.form['password']
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                user = User(address=address, city_id=city_id, name=name, phone_number=phone_number, password=hashed_password)
                models.storage.new(user)
                models.storage.save()
            except IntegrityError:
                models.storage.rollback()
                error = "Username already taken try another one"
                return render_template('signup.html', error=error, cities=cities)
            except Exception as e:
                models.storage.rollback()
                error = str(e)
                return render_template('signup.html', error=error, cities=cities)
            response = make_response(redirect(url_for('main.index')))
            session['user_id'] = user.id
            if checkauth():
                return response
            return render_template('signup.html', cities=cities)
            
    else:
        return render_template('signup.html', cities=cities)
    
@bp.route('/logout')
def logout():
    response = make_response(redirect(url_for('main.index')))
    response.delete_cookie('user_id')
    session.clear()
    return response

def checkauth():
    # user_id = request.cookies['user_id']
    user_id = session['user_id']
    print(user_id)
    if user_id:
        user = User.get(user_id)
        if user:
            session['user_id'] = user.id
            session['username'] = user.name
            session['city'] = user.city_id
            session['phone_number'] = user.phone_number
            session['address'] = user.address
            session['about'] = user.about
            return True
    return False
        