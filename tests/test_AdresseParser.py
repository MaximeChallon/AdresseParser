#!/usr/bin/python
# -*- coding: utf8 -*-

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
    adresse6 = adresse_parser.parse("1 PLACE GEORGES AGNIEL 01140 SAINT DIDIER SUR CHALARONNE")
    adresse7 = adresse_parser.parse("cité des fleurs 75018 PARIS")
    adresse8 = adresse_parser.parse("8 rond-point des Pyramides 77120 CHAMPS")
    adresse9 = adresse_parser.parse("8B rue de rivoli 75002 paris")
    adresse10 = adresse_parser.parse("8bis rue de rivoli 75002 paris")
    adresse11 = adresse_parser.parse("8 B rue de rivoli 75002 paris")
    adresse12 = adresse_parser.parse("8 bis rue de rivoli 75002 paris")

    def test_succes_parse_numero(self):
        assert self.adresse1["numero"] == str(88)
        assert self.adresse2["numero"] == str(88)
        assert self.adresse3["numero"] == str(88)
        assert self.adresse4["numero"] == str(-1)
        assert self.adresse5["numero"] == str(-1)
        assert self.adresse6["numero"] == str(1)
        assert self.adresse7["numero"] == str(-1)
        assert self.adresse8["numero"] == str(8)
        assert self.adresse9["numero"] == str('8')
        assert self.adresse10["numero"] == str('8')
        assert self.adresse11["numero"] == str('8')
        assert self.adresse12["numero"] == str('8')

        assert self.adresse1["indice"] == None
        assert self.adresse2["indice"] == None
        assert self.adresse3["indice"] == None
        assert self.adresse4["indice"] == None
        assert self.adresse5["indice"] == None
        assert self.adresse6["indice"] == None
        assert self.adresse7["indice"] == None
        assert self.adresse8["indice"] == None
        assert self.adresse9["indice"] == 'B'
        assert self.adresse10["indice"] == 'BIS'
        assert self.adresse11["indice"] == 'B'
        assert self.adresse12["indice"] == 'BIS'

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

        assert self.adresse6["rue"]["type"] == "PLACE"
        assert self.adresse6["rue"]["nom"] == "GEORGES AGNIEL"

        assert self.adresse7["rue"]["type"] == "CITÉ"
        assert self.adresse7["rue"]["nom"] == "FLEURS"

        assert self.adresse8["rue"]["type"] == "ROND-POINT"
        assert self.adresse8["rue"]["nom"] == "PYRAMIDES"

        assert self.adresse9["rue"]["type"] == "RUE"
        assert self.adresse9["rue"]["nom"] == "RIVOLI"

        assert self.adresse10["rue"]["type"] == "RUE"
        assert self.adresse10["rue"]["nom"] == "RIVOLI"

        assert self.adresse11["rue"]["type"] == "RUE"
        assert self.adresse11["rue"]["nom"] == "RIVOLI"

        assert self.adresse12["rue"]["type"] == "RUE"
        assert self.adresse12["rue"]["nom"] == "RIVOLI"

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

        assert self.adresse6["ville"]["nom"] == "SAINT DIDIER SUR CHALARONNE"

        assert self.adresse7["ville"]["arrondissement"] == 18
        assert self.adresse7["ville"]["nom"] == "PARIS"

        assert self.adresse8["ville"]["nom"] == "CHAMPS"

        assert self.adresse9["ville"]["arrondissement"] == 2
        assert self.adresse9["ville"]["nom"] == "PARIS"

        assert self.adresse10["ville"]["arrondissement"] == 2
        assert self.adresse10["ville"]["nom"] == "PARIS"

        assert self.adresse11["ville"]["arrondissement"] == 2
        assert self.adresse11["ville"]["nom"] == "PARIS"

        assert self.adresse12["ville"]["arrondissement"] == 2
        assert self.adresse12["ville"]["nom"] == "PARIS"

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

        assert self.adresse6["departement"]["numero"] == '01'
        assert self.adresse6["departement"]["nom"] == "Ain"

        assert self.adresse7["departement"]["numero"] == 75
        assert self.adresse7["departement"]["nom"] == "Paris"

        assert self.adresse8["departement"]["numero"] == 77
        assert self.adresse8["departement"]["nom"] == "Seine-et-Marne"

        assert self.adresse9["departement"]["numero"] == 75
        assert self.adresse9["departement"]["nom"] == "Paris"

        assert self.adresse10["departement"]["numero"] == 75
        assert self.adresse10["departement"]["nom"] == "Paris"

        assert self.adresse11["departement"]["numero"] == 75
        assert self.adresse11["departement"]["nom"] == "Paris"

        assert self.adresse12["departement"]["numero"] == 75
        assert self.adresse12["departement"]["nom"] == "Paris"

    def test_succes_parse_region(self):
        assert self.adresse1["region"] == "Île-de-France"

        assert self.adresse2["region"] == "Île-de-France"

        assert self.adresse3["region"] == "Île-de-France"

        assert self.adresse4["region"] == "Île-de-France"

        assert self.adresse5["region"] == "Île-de-France"

        assert self.adresse6["region"] == "Auvergne-Rhône-Alpes"

        assert self.adresse7["region"] == "Île-de-France"

        assert self.adresse8["region"] == "Île-de-France"

        assert self.adresse9["region"] == "Île-de-France"

        assert self.adresse10["region"] == "Île-de-France"

        assert self.adresse11["region"] == "Île-de-France"

        assert self.adresse12["region"] == "Île-de-France"