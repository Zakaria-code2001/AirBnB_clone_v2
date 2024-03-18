#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or Dbstorage"""
from os import getenv
from engine.db_storage import DBStorage
from engine.file_storage import FileStorage

if getenv("HBNB_TYPE_STORAGE") == 'db':
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
storage.reload()
