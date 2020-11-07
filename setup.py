# -*- coding: utf-8 -*-

################# To build the package and upload it ##################
# python3 setup.py sdist bdist_wheel
# twine upload dist/*
#######################################################################

from setuptools import setup
import AdresseParser

try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    LONG_DESCRIPTION = u"Parser d'adresses françaises"

CLASSIFIERS=[
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: French",
    "Programming Language :: Python :: 3.7",
    "Topic :: Education"
]

setup(name="AdresseParser",
      version=AdresseParser.__version__,
      description="Parser d'adresses françaises",
      long_description=LONG_DESCRIPTION,
      author="Maxime Challon",
      author_email="maxime.challon@gmail.com",
      keywords="adresse France",
      classifiers=CLASSIFIERS,
      packages=["AdresseParser"],
      test_suite='nose.collector',
      tests_require=['nose'])