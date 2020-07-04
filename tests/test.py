from unittest import TestCase
from AdresseParser import AdresseParser

"""Run python -m unittest discover tests"""

class TestAdresseParser(TestCase):
    def setUp(self) -> None:
        self.adresse_parser = AdresseParser()
        self.adresse1 = self.adresse_parser.parse("88 rue de rivoli 75002 paris")
        self.adresse2 = self.adresse_parser.parse("75002 paris 88 rue de rivoli")
        self.adresse3 = self.adresse_parser.parse("88 rue de rivoli")
        self.adresse4 = self.adresse_parser.parse("rue de rivoli 75002 paris")
        #self.adresse5 = self.adresse_parser.parse("75002 paris rue de rivoli")

    def test_succes_parse_numero(self):
        self.assertEqual(self.adresse1["numero"], str(88))

        self.assertEqual(self.adresse2["numero"], str(88))

        self.assertEqual(self.adresse3["numero"], str(88))

        self.assertEqual(self.adresse4["numero"], str(-1))

    def test_succes_parse_rue(self):
        self.assertEqual(self.adresse1["rue"]["type"], "RUE")
        self.assertEqual(self.adresse1["rue"]["nom"], "RIVOLI")

        self.assertEqual(self.adresse2["rue"]["type"], "RUE")
        self.assertEqual(self.adresse2["rue"]["nom"], "RIVOLI")

        self.assertEqual(self.adresse3["rue"]["type"], "RUE")
        self.assertEqual(self.adresse3["rue"]["nom"], "RIVOLI")

        self.assertEqual(self.adresse4["rue"]["type"], "RUE")
        self.assertEqual(self.adresse4["rue"]["nom"], "RIVOLI")

    def test_succes_parse_ville(self):
        self.assertEqual(self.adresse1["ville"]["arrondissement"], 2)
        self.assertEqual(self.adresse1["ville"]["nom"], "PARIS")

        self.assertEqual(self.adresse2["ville"]["arrondissement"], 2)
        self.assertEqual(self.adresse2["ville"]["nom"], "PARIS")

        self.assertEqual(self.adresse3["ville"]["arrondissement"], 0)
        self.assertEqual(self.adresse3["ville"]["nom"], "")

        self.assertEqual(self.adresse4["ville"]["arrondissement"], 2)
        self.assertEqual(self.adresse4["ville"]["nom"], "PARIS")