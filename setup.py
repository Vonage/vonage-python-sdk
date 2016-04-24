import re

from setuptools import setup


with open('nexmo/__init__.py', 'r') as fd:
  version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)


setup(name='nexmo',
  version=version,
  description='Nexmo Client Library for Python',
  long_description='This is the Python client library for Nexmo\'s API. To use it you\'ll need a Nexmo account. Sign up `for free at nexmo.com <http://nexmo.com?src=python-client-library>`_.',
  url='http://github.com/Nexmo/nexmo-python',
  author='Tim Craft',
  author_email='mail@timcraft.com',
  license='MIT',
  packages=['nexmo'],
  platforms=['any'],
  install_requires=['requests'])
