import importlib


def get_instance_from_string(classnames):
    classnames = [classnames] if not isinstance(classnames, list) else classnames
    instances = []
    for classname in classnames:
        try:
            module, classname = classname.rsplit('.', 1)
        except ValueError:
            raise ImportError('{} looks like not a valid module path'.format(module))
        module = importlib.import_module(module)
        try:
            instances.append(getattr(module, classname)())
        except AttributeError:
            raise ImportError('Module {} does not define {} attributr/class'.format(module, classname))
    return instances


def load_class_from_string(classnames):
    classnames = [classnames] if not isinstance(classnames, list) else classnames
    instances = []
    for classname in classnames:
        try:
            module, classname = classname.rsplit('.', 1)
        except ValueError as e:
            raise ImportError('{} looks like not a valid module path'.format(module))

        module = importlib.import_module(module)
        try:
            instances.append(getattr(module, classname))
        except AttributeError as e:
            raise ImportError('Module {} does not define {} attributr/class'.format(module, classname))
    return instances
