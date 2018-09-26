import re

from setuptools import setup

setup(
    name="nexmo",
    version="2.3.0",
    description="Nexmo Client Library for Python",
    long_description="This is the Python client library for Nexmo's API. To use it you'll need a Nexmo account. Sign up `for free at nexmo.com <http://nexmo.com?src=python-client-library>`_.",
    url="http://github.com/Nexmo/nexmo-python",
    author="Nexmo",
    author_email="devrel@nexmo.com",
    license="MIT",
    packages=["nexmo"],
    platforms=["any"],
    install_requires=["requests>=2.4.2", "PyJWT[crypto]", "pytz"],
    tests_require=["cryptography"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
