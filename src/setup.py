"""
# install it by: pip install --process-dependency-links --trusted-host guthub.com -e .
"""

import re
from os.path import join, dirname
from setuptools import setup, find_packages

# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'lutino', '__init__.py')) as v_file:
    package_version = re.compile(r".*__version__ = '(.*?)'", re.S).match(v_file.read()).group(1)

dependencies = [
    'redis',
    'ujson',
    'redlock-py',
    'hashids'
]

setup(
    name="lutino",
    version=package_version,
    author="Vahid Mardani",
    author_email="vahid@varzesh3.com",
    long_description=open(join('..', 'README.md'), encoding='UTF-8').read(),
    install_requires=dependencies,
    packages=find_packages(),
)
