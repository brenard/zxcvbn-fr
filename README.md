# zxcvbn-fr

Ce dépôt fourni une suite d'outils pour franciser la librairie de validation de la sécurité de mots de passe _zxcvbn_ (et ses variantes). Cette librairie exploite notamment un ensemble de fichiers de données de type textes correspondant à des dictionnaires de mots les plus communs. Ces dictionnaires sont fournis par les auteurs de la librairie pour la langue anglaise et ce dépôt fournis des outils pour générer leurs équivalents pour la langue française.

## data/male_names.txt & data/female_names.txt

Ces fichiers doivent contenir les prénoms les plus communément attribués aux hommes et aux femmes, triés par fréquence d'attribution (les plus fréquent en premier). Pour générer ces dictionnaires, le script _data-scripts/convert_insee_firstnames_csv_dataset_to_zxcvbn_frequency_lists.py_ exploite le [jeu de données au format CSV des prénoms produit par l'INSEE](https://www.insee.fr/fr/statistiques/2540004?sommaire=4767262) et en particulier le fichier _France hors Mayotte_. Une fois récupéré et décompressé, le fichier doit être passé en paramètre au script pour produire les fichiers _male_names.txt_ et _female_names.txt_.

Les fichiers actuellement fournis ont été générés à partir du fichier _data/nat2020.csv_ à l'aide de la commande suivante :

```
./data-scripts/convert_insee_firstnames_csv_dataset_to_zxcvbn_frequency_lists.py -p -n -L 4000 data/nat2020.csv
```

## data/french_wikipedia.txt

Ce fichier est le pendant du fichier _english_wikipedia.txt_ fourni avec la librairie _zxcvbn_ qui contient les 100 000 mots les plus fréquemment utilisés sur Wikipédia. Le fichier présent dans le dépôt a été constitué à partir de la liste des 10 000 mots les plus fréquemment utilisés sur Wikipédia France et disponible à l'adresse suivante :

https://fr.wiktionary.org/wiki/Utilisateur:Darkdadaah/Listes/Mots_dump/frwiki/2016-02-03.

__Note :__ Cette liste avait elle-même été produite à l'aide du script [get_words_from_dump.pl](https://github.com/Darkdadaah/anagrimes/blob/master/scripts/get_words_from_dump.pl) du projet [Anagrimes](https://github.com/Darkdadaah/anagrimes). Ce script doit pouvoir être utilisé pour produire une liste plus à jour.

## Copyright

Copyright (c) 2021 Benjamin Renard <brenard@zionetrix.net>

## License

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program; if not, write to the Free Software Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
