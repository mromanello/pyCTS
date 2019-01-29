import os
from setuptools import setup, find_packages

NAME = "pyCTS"
try:
    execfile('{0}/__version__.py'.format(NAME))
except NameError:
    exec(open('{0}/__version__.py'.format(NAME)).read())
VERSION = str_version


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name=NAME,
    author='Matteo Romanello',
    author_email='matteo.romanello@gmail.com',
    license='GPL v3',
    url='https://github.com/mromanello/pyCTS/',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Operating System :: POSIX'
    ],
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    long_description="pyCTS is a minimal Python implementation of the CTS URN class as defined by the Canonical Text Services protocol.",
    zip_safe=False,
)
