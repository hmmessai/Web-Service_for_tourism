import os
from dotenv import load_dotenv
from urllib.parse import quote

from flask import Flask, g
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from datetime import datetime
from flask_migrate import Migrate

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD').encode('utf-8')
db_name = os.getenv('DB_DATABASE')
db_env = os.getenv('DB_ENV')

db_url =  'mysql+mysqldb://' + db_user + ':' + quote(db_pass) + '@' + db_host + '/' + db_name

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'api.sqlite'),
        SQLALCHEMY_DATABASE_URI = db_url,
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads/'),
        STORAGE_FOLDER=os.path.join(app.instance_path, 'storage/'),
        SESSION_TYPE = 'filesystem'
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
    
    from models.user import User
    from models.city import City
    from models.place import Place

    with app.app_context():
        from . import db
        db.get_db().init_app(app)

        from . import api
        app.register_blueprint(api.bp)

        from . import main
        app.register_blueprint(main.bp)

        from . import auth
        app.register_blueprint(auth.bp)
        

        migrate = Migrate(app, g.db)
        g.bcrypt = Bcrypt(app)

        db.get_db().create_all()


    
    return app