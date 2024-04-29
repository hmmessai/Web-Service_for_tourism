import os
import json

from flask import Flask
from flask_bootstrap import Bootstrap
from datetime import datetime

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'api.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads/'),
        STORAGE_FOLDER=os.path.join(app.instance_path, 'storage/')
    )

    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    storage_folder = app.config['STORAGE_FOLDER']
    if not os.path.exists(storage_folder):
        os.makedirs(storage_folder)

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    bootstrap = Bootstrap(app)

    def datetime_to_date(datetime_string):
        return datetime_string.strftime('%B %d, %Y')


    app.jinja_env.filters['datetime_to_date'] = datetime_to_date

    @app.route('/hello')
    def hello():
        return "<h1>Hello World</h1>"
    
    from . import db
    db.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    from . import main
    app.register_blueprint(main.bp)
    
    return app