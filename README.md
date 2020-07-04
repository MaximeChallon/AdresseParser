# AddresseParser
Parser d'adresses françaises.

# Lancement

Package disponible sur [PyPI](https://pypi.org/project/AdresseParser/0.1.1/)

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
{'numero': '88', 'rue': {'type': 'RUE', 'nom': 'RIVOLI'}, 'code_postal': '75002', 'ville': {'arrondissement': 2, 'nom': 'PARIS'}, 'departement': {'numero': 75, 'nom': 'Paris'}, 'region': 'Île-de-France', 'pays': 'France'}
>>> print(result['rue'])
{'type': 'RUE', 'nom': 'RIVOLI'}
>>> print(result['ville']['arrondissement'])
2
```