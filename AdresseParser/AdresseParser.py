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
import pandas as pd
from .codes_postaux import COMMUNES
from .departements import DEPARTEMENTS
from .cedex import CEDEX

class AdresseParser():
    def __init__(self):
        self.regex_rue = '((AVENUE|IMPASSE|QUAI|VOIE|RUELLE|PLACE|BOULEVARD|RUE|VOIE|CIT(E|É)|ALL(É|E)E|CHEMIN|ROUTE|GR|R(É|E)SIDENCE|HAMEAU|LIEU(-| )DIT|TRAVERSE|PROMENADE|ROND(-| )POINT|PASSAGE)( D(E(S?| LA)|U))? )'
        self.type_rue = ['rue', 'avenue', 'boulevard', 'impasse', 'quai', 'voie', 'place', 'ruelle', 'cour', 'cité', 'cite', 'allée','allee','chemin','lieu-dit','promenade','lieu dit','rond point', 'rond-point', 'passage','traverse','route','gr','résidence','residence','hameau']
        self.cedex = pd.DataFrame(CEDEX)

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
        cedex = self.get_cedex(bloc_ville, code_postal)

        numero, indice = self.get_numero_rue(bloc_rue)
        
        dict_adresse = {
            "numero": numero,
            "indice":indice,
            "rue":{
                "type": type_rue,
                "nom": nom_rue
            },
            "code_postal": code_postal,
            "ville": {
                "arrondissement": arrondissement,
                "nom": ville
            },
            "cedex":cedex,
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
        # vérification de la présence d'un cedex dans l'adresse en premier lieu
        if "cedex" in requete.lower():
            if re.match("^[0-9]{0,4}.*[0-9]{5}.*$", requete):
                bloc_rue = re.sub("[0-9]{5}.*", "", requete)
                bloc_ville = re.match("^[0-9]{0,4}.*([0-9]{5}.*)$", requete).group(1)

        else:
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
        Permet d'extraire le numéro de la rue et son indice
        :param bloc_rue: string avec le numéro et le nom de la rue
        :return: tuple(str, str)
        """
        source_indice = ["B", "BI", "BIS", "T", "TE", "TER", "C", "Q", "QUATER", "D"]
        cible_indice = ["BIS", "BIS", "BIS", "TER", "TER", "TER", "TER", "QUATER", "QUATER", "QUATER"]
        regex = "^(([0-9]+)( ?(B|b|bis|BIS|t|T|ter|TER|quater|QUATER|C|D|E|c|d|e|f|F) )?) ?(.+)?"
        if re.match(regex, bloc_rue):
            tmp = str(re.match(regex, bloc_rue).group(1)).replace(" ","").lower()
            numero_rue = re.sub(r'[^0-9\-]', '', tmp)
            indice = str(re.sub(r'[0-9\-]', '', tmp)).upper()
            if indice == '':
                indice = None
            else:
                try:
                    indice = cible_indice[source_indice.index(indice)]
                except:
                    indice = indice
        else:
            numero_rue = str(-1)
            indice = None

        return numero_rue, indice

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

            if re.match("[0-9]{5} ?[^0-9]+(cedex.*)?$", str(bloc_ville).lower()):
                ville = re.sub("[0-9]{5} ?", "", str(bloc_ville))
                ville = re.sub(" ?cedex.*", "", str(ville).lower())
                ville = ville.upper().rstrip()
            else:
                ville = COMMUNES[str(code_postal)].upper().rstrip()

            if "PARIS" in ville or "LYON" in bloc_ville or "MARSEILLE" in bloc_ville or re.match('^75[0-9]{3}', code_postal):
                arrondissement = int(re.sub("^0+", "", code_postal.replace('75', '')))
                if arrondissement>20:
                    arrondissement = 0
            else:
                arrondissement = 0
        else:
            arrondissement = 0
            ville = ""

        return ville, arrondissement

    def get_cedex(self, bloc_ville, code_postal):
        """
        Extrait le cedex s'il existe
        :param bloc_ville: string 
        :param code_postal: string
        :return: str
        """
        cedex = []
        if bloc_ville:
            if "cedex" in bloc_ville.lower():
                try:
                    result  = self.cedex[self.cedex['cedex'] == int(code_postal)]
                    for index, row in result.iterrows():
                        cedex.append({"libelle":row[1], "code_insee":str(row[2])})
                except:
                    pass
        return cedex

    def compare(self, adresse1:str, adresse2:str, clean_stopwords:bool = False):
        """
        Compare les deux adresses données en entrée
        :param adresse1: string , première adresse à comparer
        :param adresse2: string, deuxième adresse à comparer
        :param clean_stopwords: boolean, si True, effectue la comparaison en enlevant les stopwords de la rue
        :return: bool
        """
        identique = False
        adresse1 = self.parse(adresse1)
        adresse2 = self.parse(adresse2)
        regex_stop = r'((^| )((AU)|(DE)|(DES)|(DU)|(EN)|(LA)|(LE)|(LES)|(SON)|(SUR))) '
        if clean_stopwords:
            adresse1["rue"]["nom"] = re.sub(regex_stop, '', adresse1["rue"]["nom"])
            adresse2["rue"]["nom"] = re.sub(regex_stop, '', adresse2["rue"]["nom"])
        if adresse1 == adresse2:
            identique =True
        return identique