![GitHub](https://img.shields.io/github/license/MaximeChallon/AdresseParser?logo=License)
![GitHub contributors](https://img.shields.io/github/contributors/MaximeChallon/AdresseParser)
![Python package](https://github.com/MaximeChallon/AdresseParser/workflows/Python%20package/badge.svg?branch=master)
![PyPI](https://img.shields.io/pypi/v/AdresseParser)
![PyPI - Format](https://img.shields.io/pypi/format/AdresseParser?label=PyPi%20format)
[![Build Status](https://travis-ci.org/MaximeChallon/AdresseParser.svg?branch=master)](https://travis-ci.org/MaximeChallon/AdresseParser)
![GitHub Release Date](https://img.shields.io/github/release-date/MaximeChallon/AdresseParser)

# AddresseParser
Package Python pour parser et comparer les adresses françaises.

# Lancement

Package disponible sur [PyPI](https://pypi.org/project/AdresseParser)

Vous pouvez l'installer avec pip:
```bash
pip install AdresseParser
```
Exemple d'utilisation en console Python:
```bash
>>> from AdresseParser import AdresseParser
>>> adr_parser = AdresseParser()
>>> result = adr_parser.parse("88 rue de rivoli 75002 paris")
>>> print(result)
{'numero': '88', 'indice': None, 'rue': {'type': 'RUE', 'nom': 'RIVOLI'}, 'code_postal': '75002', 'ville': {'arrondissement': 2, 'nom': 'PARIS'}, 'cedex': [], 'departement': {'numero': 75, 'nom': 'Paris'}, 'region': 'Île-de-France', 'pays': 'France'}
>>> print(result['rue'])
{'type': 'RUE', 'nom': 'RIVOLI'}
>>> print(result['ville']['arrondissement'])
2
```

# Return

```json
{
    "numero": "str",
    "indice": "str",
    "rue":{
          "type": "str",
          "nom": "str"
     },
    "code_postal": "str",
    "ville": {
          "arrondissement": "int",
          "nom": "str"
     },
     "cedex":[
       {
        "libelle": "str",
        "codde_insee": "str"
       }
     ],
    "departement": {
          "numero": "str",
          "nom": "str"
     },
    "region": "str",
    "pays": "France"
 }
```
