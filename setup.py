import os
from setuptools import setup

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name='python_jwt',
    version='1.2.1',
    description="Module for generating and verifying JSON Web Tokens",
    long_description=read('README.rst'),
    keywords='',
    author='David Halls',
    author_email='dave@davedoesdev.com',
    url='https://github.com/davedoesdev/python-jwt',
    license='MIT',
    packages=['jwt'],
    install_requires=['jws>=0.1.3'],
)
