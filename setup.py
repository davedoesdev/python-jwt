import os
from setuptools import setup

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name='python_jwt',
    version='3.1.0',
    description="Module for generating and verifying JSON Web Tokens",
    long_description=read('README.rst'),
    keywords='',
    author='David Halls',
    author_email='dave@davedoesdev.com',
    url='https://github.com/davedoesdev/python-jwt',
    license='MIT',
    packages=['python_jwt'],
    install_requires=['jwcrypto>=0.4.2'],
)
