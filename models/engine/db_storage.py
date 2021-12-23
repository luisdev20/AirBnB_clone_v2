#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from models.base_model import Base
from os import getenv
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import unittest
import models


class DBStorage:
    """This class manages storage of hbnb models in MySQL format"""
    __engine = None
    __session = None

    def __init__(self):
        connection = 'mysql+mysqldb://{}:{}@{}/{}'\
                .format(getenv('HBNB_MYSQL_USER'),
                        getenv('HBNB_MYSQL_PWD'),
                        getenv('HBNB_MYSQL_HOST'),
                        getenv('HBNB_MYSQL_DB'))
        self.__engine = create_engine(connection, pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary from a database query"""
        clsDict = {}
        if cls:
            lstobj = self.__session.query(eval(cls)).all()
            for obj in lstobj:
                clsname = type(obj).__name__
                clsstr = "{}.{}".format(clsname, obj.id)
                clsDict[clsstr] = obj
        else:
            for sub_c in Base.__subclasses__():
                table = self.__session.query(sub_c).all()
                for obj in table:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    clsDict[key] = obj
        return clsDict

    def new(self, obj):
        """Add new object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and starts the current database
        session from the engine"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Closes the session"""
        self.__session.close()
