import io
import os

from setuptools import setup, find_packages


with io.open(
    os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8"
) as f:
    long_description = f.read()

setup(
    name="vonage",
    version="4.0.0b0",
    description="Vonage Server SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Vonage/vonage-python-sdk",
    author="Vonage",
    author_email="devrel@vonage.com",
    license="Apache",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    platforms=["any"],
    install_requires=[
        "requests>=2.4.2",
        "PyJWT[crypto]>=1.6.4",
        "pytz>=2018.5",
        "Deprecated",
    ],
    python_requires=">=3.7",
    tests_require=["cryptography>=2.3.1"],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
