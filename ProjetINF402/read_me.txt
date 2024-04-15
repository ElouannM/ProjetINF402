compiler + resultat:
python3 main.py grilletest/board1.txt

Manuel:
python3 main.py -h

Que creer le fichier dimacs:
python3 main.py -f grilletest/board1.txt

Que le resultat du sat solver:
python3 main.py -s grilletest/board1.txt

Transformation du resultat du sat solver
python3 main.py -t grilletest/board1.txt

Pas d'option = tout
Si appelle 


juste resultat du sat solver : 
cryptominisat5 --verb=0 output.cnf


Requirements:
https://pypi.org/project/pycryptosat/