import os
from setuptools import setup, find_packages

VERSION = "0.1.0"
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='pyCTS',
	author='Matteo Romanello',
	author_email='matteo.romanello@gmail.com',
	url='https://github.com/mromanello/CTS_dev/',
    version=VERSION,
    packages=find_packages(),
    include_package_data=True,
    long_description=read('README.txt'),
    #install_requires=['partitioner','CRFPP'],
    zip_safe=False,
)