import re

from setuptools import setup


with open('nexmo/__init__.py', 'r') as fd:
  version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)


setup(name='nexmo',
  version=version,
  description='Python client for the Nexmo API',
  long_description='Python client for the Nexmo API',
  url='http://github.com/Nexmo/nexmo-python',
  author='Tim Craft',
  author_email='mail@timcraft.com',
  license='MIT',
  packages=['nexmo'],
  platforms=['any'],
  install_requires=['requests'])
