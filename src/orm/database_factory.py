# coding: utf-8

from ..util.dynamic_import import load_class_from_string as classloader
from ..conf import setting

import time
import threading


class DatabaseFactory:

    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.instances = {}
        time.sleep(1)

    def __database(self, db):
        name = setting.database[db]['name']
        config = setting.database[db]['config']
        try:
            classname = classloader(name)[0]
            instance = classname(**config)
            instance.connect()
            self.instances[db] = instance
        except Exception:
            raise

    def get_conn(self, database):
        if database not in self.instances:
            self.__database(database)
        return self.instances[database]

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(DatabaseFactory, "_instance"):
            with DatabaseFactory._instance_lock:
                if not hasattr(DatabaseFactory, "_instance"):
                    DatabaseFactory._instance = \
                            DatabaseFactory(*args, **kwargs)
        return DatabaseFactory._instance
