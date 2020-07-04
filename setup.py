# -*- coding: utf-8 -*-

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
      install_requires=[])