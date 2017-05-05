import os
from setuptools import setup, find_packages

NAME = "pyCTS"
try:
    execfile('{0}/__version__.py'.format(NAME))
except NameError as e:
    exec(open('{0}/__version__.py'.format(NAME)).read())
VERSION = str_version

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name=NAME,
    author='Matteo Romanello',
    author_email='matteo.romanello@gmail.com',
    license='GPL v3',
    url='https://github.com/mromanello/pyCTS/',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Operating System :: POSIX'
    ],
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    zip_safe=False,
)
