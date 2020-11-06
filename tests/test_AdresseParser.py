#from unittest import TestCase
from AdresseParser import AdresseParser
import pytest

"""Run python -m unittest discover tests"""
"""Run pytest -v"""

class TestAdresseParser():
    adresse_parser = AdresseParser()
    adresse1 = adresse_parser.parse("88 rue de rivoli 75002 paris")
    adresse2 = adresse_parser.parse("75002 paris 88 rue de rivoli")
    adresse3 = adresse_parser.parse("88 rue de rivoli")
    adresse4 = adresse_parser.parse("rue de rivoli 75002 paris")
    adresse5 = adresse_parser.parse("75002 paris rue de rivoli")

    def test_succes_parse_numero(self):
        assert self.adresse1["numero"] == str(88)

        assert self.adresse2["numero"] == str(88)

        assert self.adresse3["numero"] == str(88)

        assert self.adresse4["numero"] == str(-1)

        assert self.adresse5["numero"] == str(-1)

    def test_succes_parse_rue(self):
        assert self.adresse1["rue"]["type"] == "RUE"
        assert self.adresse1["rue"]["nom"] == "RIVOLI"

        assert self.adresse2["rue"]["type"] == "RUE"
        assert self.adresse2["rue"]["nom"] == "RIVOLI"

        assert self.adresse3["rue"]["type"] == "RUE"
        assert self.adresse3["rue"]["nom"] == "RIVOLI"

        assert self.adresse4["rue"]["type"] == "RUE"
        assert self.adresse4["rue"]["nom"] == "RIVOLI"

        assert self.adresse5["rue"]["type"] == "RUE"
        assert self.adresse5["rue"]["nom"] == "RIVOLI"

    def test_succes_parse_ville(self):
        assert self.adresse1["ville"]["arrondissement"] == 2
        assert self.adresse1["ville"]["nom"] == "PARIS"

        assert self.adresse2["ville"]["arrondissement"] == 2
        assert self.adresse2["ville"]["nom"] == "PARIS"

        assert self.adresse3["ville"]["arrondissement"] == 0
        assert self.adresse3["ville"]["nom"] == ""

        assert self.adresse4["ville"]["arrondissement"] == 2
        assert self.adresse4["ville"]["nom"] == "PARIS"

        assert self.adresse5["ville"]["arrondissement"] == 2
        assert self.adresse5["ville"]["nom"] == "PARIS"

    def test_succes_parse_departement(self):
        assert self.adresse1["departement"]["numero"] == 75
        assert self.adresse1["departement"]["nom"] == "Paris"

        assert self.adresse2["departement"]["numero"] == 75
        assert self.adresse2["departement"]["nom"] == "Paris"

        assert self.adresse3["departement"]["numero"] == 75
        assert self.adresse3["departement"]["nom"] == "Paris"

        assert self.adresse4["departement"]["numero"] == 75
        assert self.adresse4["departement"]["nom"] == "Paris"

        assert self.adresse5["departement"]["numero"] == 75
        assert self.adresse5["departement"]["nom"] == "Paris"

    def test_succes_parse_region(self):
        assert self.adresse1["region"] == "Île-de-France"

        assert self.adresse2["region"] == "Île-de-France"

        assert self.adresse3["region"] == "Île-de-France"

        assert self.adresse4["region"] == "Île-de-France"

        assert self.adresse5["region"] == "Île-de-France"