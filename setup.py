import io
import os

from setuptools import setup, find_packages


with io.open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="nexmo",
    version="2.5.2",
    description="Nexmo Client Library for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Nexmo/nexmo-python",
    author="Nexmo",
    author_email="devrel@nexmo.com",
    license="MIT",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    platforms=["any"],
    install_requires=[
        "requests>=2.4.2",
        "PyJWT[crypto]>=1.6.4",
        "pytz>=2018.5",
        "Deprecated",
    ],
    python_requires=">=3, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    tests_require=["cryptography>=2.3.1"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
