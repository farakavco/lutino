import importlib
import importlib.util
import sys
import warnings
from os.path import dirname, abspath
from base64 import urlsafe_b64decode

try:
    import re2 as re
except ImportError:
    import re


def import_python_module_by_filename(name, module_filename):
    """
    Import's a file as a python module, with specified name.

    Don't ask about the `name` argument, it's required.
    
    :param name: The name of the module to override upon imported filename.
    :param module_filename: The filename to import as a python module.
    :return: The newly imported python module.
    """

    sys.path.append(abspath(dirname(module_filename)))
    spec = importlib.util.spec_from_file_location(
        name,
        location=module_filename)
    imported_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imported_module)
    return imported_module


def get_class_by_name(name):
    parts = name.split('.')
    module_name, class_name = '.'.join(parts[:-1]), parts[-1]
    module_ = importlib.import_module(module_name)
    return getattr(module_, class_name)


def construct_class_by_name(name, *args, **kwargs):
    """
    Construct a class by module path name using *args and **kwargs

    Don't ask about the `name` argument, it's required.

    :param name: class name
    :return: The newly imported python module.
    """
    return get_class_by_name(name)(*args, **kwargs)


def deprecated(func):
    """
    This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used.
    """

    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # Turn off filter
        warnings.warn(
            'Call to deprecated function %s.' % func.__name__,
            category=DeprecationWarning,
            stacklevel=2
        )
        warnings.simplefilter('default', DeprecationWarning)  # Reset filter
        return func(*args, **kwargs)

    new_func.__name__ = func.__name__
    new_func.__doc__ = func.__doc__
    new_func.__dict__.update(func.__dict__)
    return new_func


def natural_sort(l, key=None, reverse=False):
    """
    Natural sort a list via specified key.
    """
    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(sort_key):
        nonlocal key
        sort_key = key(sort_key) if key is not None else sort_key
        return [convert(c) for c in re.split('([0-9]+)', sort_key)]

    return sorted(l, key=alphanum_key, reverse=reverse)


def normalize_b64urlsafe(content):
    padding_check = len(content) % 4

    if padding_check == 1:
        raise ValueError
    elif padding_check == 2:
        content += '=='
    elif padding_check == 3:
        content += '='

    return urlsafe_b64decode(content).decode()
