import os
from urllib.parse import quote
from dotenv import load_dotenv
from models.basemodel import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.city import City
from models.place import Place
from models.user import User

load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_pass = os.getenv('DB_PASSWORD').encode('utf-8')
db_name = os.getenv('DB_DATABASE')
db_env = os.getenv('DB_ENV')

classes = {
    'City': City,
    'Place': Place,
    'User': User
}

class DBStorage:
    """Represents DBStorage"""

    __engine = None
    __session = None

    def __init__(self):
        db_url =  'mysql+mysqldb://' + db_user + ':' + quote(db_pass) + '@' + db_host + '/' + db_name
        self.__engine = create_engine(db_url, pool_pre_ping=True)

    def all(self, cls=None):
        dic = {}
        if cls:
            if cls in classes:
                objs = self.__session.query(classes[cls]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dic[key] = obj
        else:
            for i in classes:
                objs = self.__session.query(classes[i]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dic[key] = obj
        return dic

    def new(self, obj):
        self.__session.add(obj)

    def save(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def delete(self, obj=None):
        if obj is not None:
            self.__session.delete(obj)


    def reload(self):
        Base.metadata.create_all(self.__engine, checkfirst=True)
        # print('creating .....' + str(globals()['__name__']) )
        # print('\033[91m') 
        # print(Base.metadata.tables)
        # print(self.__engine)
        # print('\033[0m')
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory=session_factory)