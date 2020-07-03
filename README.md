#PyAddresseParser
Parser et formatter des addresses françaises.

#Lancement
```
>>> from AdresseParser import adresse_parser
>>> adr_parser = adresse_parser.AdresseParser()
>>> print(adr_parser.parse("88 rue de rivoli 75000 paris"))
('88 rue de rivoli ', '75000 paris')
```