# -*- coding: utf-8 -*-
import importlib.util
import sys
from os.path import dirname, abspath
__author__ = 'vahid'


def import_python_module_by_filename(name, module_filename):
    sys.path.append(abspath(dirname(module_filename)))
    spec = importlib.util.spec_from_file_location(
        name,
        location=module_filename)
    imported_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imported_module)
    return imported_module
