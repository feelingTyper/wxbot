# coding: utf-8

import time
import threading
import importlib


class Container:
    _instance_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.instances = {}
        time.sleep(1)

    @classmethod
    def instance(cls, *args, **kwargs):
        if not hasattr(Container, "_instance"):
            with Container._instance_lock:
                if not hasattr(Container, "_instance"):
                    Container._instance = \
                            Container(*args, **kwargs)
        return Container._instance

    def singleten(self, classname, *args, **kwargs):
        return self.singletens(classname, *args, **kwargs)[0]

    def singletens(self, classnames, *args, **kwargs):
        classnames = [classnames] if not isinstance(classnames, list) \
                else classnames
        instances = []
        for classname in classnames:
            if classname in self.instances:
                instances.append(self.instances.get(classname))
                continue
            try:
                module, classname = classname.rsplit('.', 1)
            except ValueError:
                raise ImportError(
                        '{} looks like not a valid module path'.
                        format(module))
            module = importlib.import_module(module)
            try:
                inst = getattr(module, classname)(*args, **kwargs)
                instances.append(self.instances.setdefault(classname, inst))
            except AttributeError:
                raise ImportError(
                        'Module {} does not define {} attributr/class'.
                        format(module, classname))
        return instances

    @staticmethod
    def classLoader(classnames):
        classnames = [classnames] if not isinstance(classnames, list) \
                else classnames
        instances = []
        for classname in classnames:
            try:
                module, classname = classname.rsplit('.', 1)
            except ValueError:
                raise ImportError(
                        '{} looks like not a valid module path'.format(module))

            module = importlib.import_module(module)
            try:
                instances.append(getattr(module, classname))
            except AttributeError:
                raise ImportError(
                        'Module {} does not define {} attributr/class'.
                        format(module, classname))
        return instances
