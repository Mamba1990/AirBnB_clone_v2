#!/usr/bin/python3
""" Module representing Database Storage """
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.amenity import Amenity


class DBStorage:
    """
    Class handles database engine
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Function creates engine for database
        """
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('HBNB_MYSQL_USER'),
            getenv('HBNB_MYSQL_PWD'),
            getenv('HBNB_MYSQL_HOST'),
            getenv('HBNB_MYSQL_DB')),
            pool_pre_ping=True
        )

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Handles query for all objects on the
        current database session
        """
        classes = {
            "City": City,
            "State": State,
            "User": User,
            "Place": Place,
            "Review": Review,
            "Amenity": Amenity,
        }
        res = {}
        query_rows = []

        if cls:
            """ a query for all cls' objects """
            if type(cls) is str:
                cls = eval(cls)
            query_rows = self.__session.query(cls)
            for obj in query_rows:
                key = '{}.{}'.format(type(obj).__name__, obj.id)
                res[key] = obj
            return res
        else:
            """a query for all objects"""
            for name, value in classes.items():
                query_rows = self.__session.query(value)
                for obj in query_rows:
                    key = '{}.{}'.format(name, obj.id)
                    res[key] = obj
            return res

    def new(self, obj):
        """Adding object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """func commiting all changes of the
        current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deleting obj from the current database session"""
        self.__session.delete(obj)

    def reload(self):
        """
         Creates all tables in the database
         Creates the current database session from the engine
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        function to closee
        """
        self.__session.close()
