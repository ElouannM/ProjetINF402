Manuel:
python3 main.py -h

-Uniquement creer le fichier dimacs:
python3 main.py -f grilletest/board1.txt

-Uniquement le resultat du sat solver:
python3 main.py -s grilletest/board1.txt

-Transformation du resultat du sat solver:
python3 main.py -t grilletest/board1.txt

-Pas d'option = tout :
python3 main.py grilletest/board1.txt


-Juste resultat du sat solver(le fichier DIMACS doit etre creer avant) : 
cryptominisat5 --verb=0 output.cnf


Requirements:
https://pypi.org/project/pycryptosat/

Les grille de test sont dans le rep grilletest/
