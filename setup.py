from setuptools import setup

try:
    LONG_DESCRIPTION = open('README.md').read()
except:
    LONG_DESCRIPTION = u"Parser et formatter d'adresses françaises"

CLASSIFIERS=[
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: French",
    "Programming Language :: Python :: 3.7",
    "Topic :: Education"
]

setup(name="PyAdresseParser",
      version="0.0.1",
      description="Parser et formatter d'adresses françaises",
      long_description=LONG_DESCRIPTION,
      author="Maxime Challon",
      author_email="maxime.challon@gmail.com",
      keywords="adresse France",
      classifiers=CLASSIFIERS,
      url="",
      packages=["AdresseParser"],
      install_requires=[])