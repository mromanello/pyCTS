import os
from setuptools import setup, find_packages
import pyCTS

VERSION = pyCTS.__version__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pyCTS',
	author='Matteo Romanello',
	author_email='matteo.romanello@gmail.com',
	url='https://github.com/mromanello/pyCTS/',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.md'),
    #install_requires=['partitioner','CRFPP'],
    zip_safe=False,
)
