import dist.bentomaker
import setuptools
from bento.distutils.monkey_patch import monkey_patch
monkey_patch()

from setuptools import setup

if __name__ == '__main__':
    setup()
