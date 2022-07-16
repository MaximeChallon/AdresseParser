#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    AdresseParser.AdresseParser
    Parser d'adresses françaises.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    :copyright: (c) 2020 by Maxime Challon.
    :license: MIT, see LICENSE for more details.
"""

import re
from .codes_postaux import COMMUNES
from .departements import DEPARTEMENTS

class AdresseParser():
    def __init__(self):
        self.regex_rue = '((AVENUE|IMPASSE|QUAI|VOIE|RUELLE|PLACE|BOULEVARD|RUE|VOIE|CIT(E|É)|ALL(É|E)E|CHEMIN|ROUTE|GR|R(É|E)SIDENCE|HAMEAU|LIEU(-| )DIT|TRAVERSE|PROMENADE|ROND(-| )POINT|PASSAGE)( D(E(S?| LA)|U))? )'
        self.type_rue = ['rue', 'avenue', 'boulevard', 'impasse', 'quai', 'voie', 'place', 'ruelle', 'cour', 'cité', 'cite', 'allée','allee','chemin','lieu-dit','promenade','lieu dit','rond point', 'rond-point', 'passage','traverse','route','gr','résidence','residence','hameau']

    def parse(self, adresse_string):
        """
        Parse la chaîne mise en paramètre et retourne un dictionnaire
        :param adresse_string: chaîne de caractères de l'adresse
        :return: dict
        """
        bloc_rue, bloc_ville = self.blocs(adresse_string)

        nom_rue, type_rue = self.get_nom_type_rue(bloc_rue)
        ville, arrondissement = self.get_ville(bloc_ville)

        code_postal, numero_dpt = self.get_code_postal(bloc_ville)
        
        dict_adresse = {
            "numero": self.get_numero_rue(bloc_rue),
            "rue":{
                "type": type_rue,
                "nom": nom_rue
            },
            "code_postal": code_postal,
            "ville": {
                "arrondissement": arrondissement,
                "nom": ville
            },
            "departement": {
                "numero": numero_dpt,
                "nom": DEPARTEMENTS[str(numero_dpt)]["nom"]
            },
            "region": DEPARTEMENTS[str(numero_dpt)]["region"]["nom"],
            "pays": "France"
        }

        return dict_adresse

    def blocs(self, adresse_string):
        """
            Permet d'extraire l'adresse' de la requête de l'utilisateur
            :param requete: requête faite dans l'api
            :return: str
            """
        # retournement de l'adresse donnée en string pour la mettre sous la forme Numéro_rue Rue Code_postal Ville
        # si le code postal est au début
        if re.match("^[0-9]{5}[a-zA-Z éèàùêôî-]{0,}[0-9]{1,4}(.+)$", adresse_string):
            pattern = "^([0-9]{5}[a-zA-Z éèàùêôî-]{0,})([0-9]{0,4}.+)$"
            requete = re.match(pattern, adresse_string).group(2) +" "+ re.match(pattern, adresse_string).group(1)

        # si le bloc_ville est au début et qu'il n'y a pas de numéro de rue
        elif re.match("[0-9]{5} ?.+ ?([r|R]ue|RUE|[a|A]venue|AVENUE|[b|B]oulevard|BOULEVARD|QUAI|[q|Q]uai|PLACE|[p|P]lace).+", adresse_string):
            pattern = "^([0-9]{5} ?.+) ?(([r|R]ue|RUE|[a|A]venue|AVENUE|[b|B]oulevard|BOULEVARD|QUAI|[q|Q]uai|PLACE|[p|P]lace).+)$"
            requete = re.match(pattern, adresse_string).group(2) + " " + re.match(pattern, adresse_string).group(1)

        # si le code postal est en deuxième partie
        elif re.match("^[0-9]{0,4}.*[0-9]{5}[a-zA-Z éèàùêôî-]{0,}$", adresse_string):
            requete = adresse_string

        else:
            requete = adresse_string

        # à partir de l'adresse normalisée, extraction des différents blocs d'information
        if re.match("^[0-9]{0,4}.*[0-9]{5}[a-zA-Z éèàùêôî-]{0,}$", requete):
            bloc_rue = re.sub("[0-9]{5}.*", "", requete)
            bloc_ville = re.match("^[0-9]{0,4}.*([0-9]{5}[a-zA-Z éèàùêôî-]{0,})$", requete).group(1)

        elif re.match("^[0-9]{0,4}.*$", requete):
            bloc_rue = re.sub("[0-9]{5}.*", "", requete)
            bloc_ville = re.match("^([0-9]{5}[a-zA-Z éèàùêôî-]{0,})[0-9]{0,4}.*$", requete)
            if bloc_ville is not None:
                bloc_ville = bloc_ville.group(1)

        return (bloc_rue, bloc_ville)

    def get_numero_rue(self, bloc_rue):
        """
        Permet d'extraire le numéro de la rue
        :param bloc_rue: string avec le numéro et le nom de la rue
        :return: str
        """
        #ancien : ^([0-9]+) ?(.+)?
        if re.match("^(([0-9]+)( ?(B|b|bis|BIS|t|T|ter|TER|quater|QUATER|C|D|E|c|d|e|f|F) )?) ?(.+)?", bloc_rue):
            numero_rue = str(re.match("^(([0-9]+)( ?(B|b|bis|BIS|t|T|ter|TER|quater|QUATER|C|D|E|c|d|e|f|F) )?) ?(.+)?", bloc_rue).group(1)).replace(" ","").lower()
        else:
            numero_rue = str(-1)

        return numero_rue

    def get_nom_type_rue(self, bloc_rue):
        """
        Permet d'extraire le nom et le type de la rue
        :param bloc_rue: string avec le numéro et le nom de la rue
        :return: str
        """
        nom_rue = re.sub(self.regex_rue, "", re.sub("(([0-9]+)( ?(B|b|bis|BIS|t|T|ter|TER|quater|QUATER|C|D|E|c|d|e|f|F) )?) ?", "", bloc_rue.upper()))
        nom_rue = re.sub(" +$", "", nom_rue)

        type = ""

        for type_rue in self.type_rue:
            if (type_rue + " ") in bloc_rue.lower():
                type = type_rue.upper()

        return nom_rue, type

    def get_code_postal(self, bloc_ville):
        """
        Extrait le code postal s'il existe
        :param bloc_ville: string avec code postal et ville
        :return: int
        """
        if re.match("([0-9]{5}) ?([^0-9]+)?", str(bloc_ville)):
            code_postal = re.match("([0-9]{5}) ?([^0-9]+)?", bloc_ville).group(1)
        else:
            code_postal = "75001"

        numero_dpt = int(re.sub('[0-9]{3}$', '', str(code_postal)))
        if int(numero_dpt) < 10:
            numero_dpt = "0" + str(numero_dpt)
        if 20000 <= int(code_postal) < 21000:
            if int(code_postal) <= 20190:
                numero_dpt = "2A"
            else:
                numero_dpt = "2B"

        return code_postal, numero_dpt

    def get_ville(self, bloc_ville):
        """
        Extrait la ville et l'arrondissement si nécessaire
        :param bloc_ville: string avec le code postal et la ville
        :return: str
        """
        if bloc_ville is not None:
            code_postal, numero_dpt = self.get_code_postal(bloc_ville)

            if re.match("[0-9]{5} ?[^0-9]+$", str(bloc_ville)):
                ville = re.sub("[0-9]{5} ?", "", str(bloc_ville))
                ville = ville.upper().rstrip()
            else:
                ville = COMMUNES[str(code_postal)].upper().rstrip()

            if "PARIS" in ville or "LYON" in bloc_ville or "MARSEILLE" in bloc_ville or re.match('^75[0-9]{3}', code_postal):
                arrondissement = int(re.sub("^0+", "", code_postal.replace('75', '')))
            else:
                arrondissement = 0
        else:
            arrondissement = 0
            ville = ""

        return ville, arrondissement