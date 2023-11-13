import os
from setuptools import setup

def read(name):
    return open(os.path.join(os.path.dirname(__file__), name)).read()

setup(
    name='python_jwt',
    version='4.1.0',
    description="Module for generating and verifying JSON Web Tokens",
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='',
    author='David Halls',
    author_email='dave@davedoesdev.com',
    url='https://github.com/davedoesdev/python-jwt',
    license='MIT',
    packages=['python_jwt'],
    install_requires=['jwcrypto>=1.4.2'],
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
)
