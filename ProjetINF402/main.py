import sys
import subprocess
#import argparse




#fpnction qui prend un fichier representant une grille du jeu et la transforme en tableau en enlevant les saut de ligne, chaque ligne devient une string
def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            return f.read().split('\n')
    except FileNotFoundError:
        print("chemin invalide")
        sys.exit(1)




#A partir d'un tableau représentant une grille creer a partir de la fonction read_file(), creer un tableau contenant les cases 
#et un autre tableau contenant les contraintes sous forme de tableau de couple contenant comme 1er couple 
#les coordonées de la case devant contenir une valeur plus grande que la deuxiéme
def get_grid(board_rows):
    global n  #taille de la grille, var globale

    def h(i, j):
        return (i // 2), (j // 2)

    tiles, constraints, n = [], [], (len(board_rows) + 1) // 2

    for i in range(len(board_rows)):
        if i % 2 == 0:      #si i pair, on traite une ligne de cases et avec les contraintes < et > possibles
            ll = []
            for j in range(len(board_rows[i])):
                if board_rows[i][j] == '<':
                    constraints.append([h(i, j + 1), h(i, j - 1)])
                elif board_rows[i][j] == '>':
                    constraints.append([h(i, j - 1), h(i, j + 1)])
                elif board_rows[i][j] != ' ':
                    ll.append(board_rows[i][j])
            tiles.append(ll)
        else:
            for j in range(len(board_rows[i])):
                if board_rows[i][j] == '^':
                    constraints.append([h(i + 1, j), h(i - 1, j)])
                if board_rows[i][j] == 'v' or board_rows[i][j] == 'V':
                    constraints.append([h(i, j), h(i + 1, j)])
    return tiles, constraints



#pour assigner une variable format dimacs
def var(r, c, v):
    assert (0 <= r and r <= n and 0 <= c and c <= n and 1 <= v and v < n+1)#verifier que la case est valide
    return (r - 1) * n * n + (c - 1) * n + (v - 1) + 1


def clauses(t, constraints):
    cls = []  #liste des clauses
    for r in range(1,n+1): 
        for c in range(1, n+1):
            # chaque case a au moins une valeur
            cls.append([var(r,c,v) for v in range(1,n+1)])
            # chaque case a au plus une valeur
            for v in range(1, n+1):
                for w in range(v+1,n+1):
                    cls.append([-var(r,c,v), -var(r,c,w)])  #chaque case a au plus une valeur
    for v in range(1, n + 1):
        for l in range(1, n + 1):  cls.append([var(l, c, v) for c in range(1, n + 1)])  #chaque ligne a la valeur v
        for c in range(1, n + 1): cls.append([var(l, c, v) for l in range(1, n + 1)])  #chaque colonne a la valeur v
    #ajouter les cases deja données dans la grille
    for l in range(1, n + 1):
        for c in range(1, n + 1):
            if t[l - 1][c - 1].isdigit():
                cls.append([var(l, c, int(t[l - 1][c - 1]))])
    #Contraintes
    for x in constraints :
        (a, b) = x
        (i1, j1) = a
        (i2, j2) = b
        for v in range(1, n ):
            for w in range(v + 1, n + 1):
                cls.append([-var(i1+1, j1+1, v), -var(i2+1, j2+1, w)])
    return cls


def solve_with_file(file_name):
    board = read_file(file_name)
   # print(board)
    tiles, constraints = get_grid(board)
    #print("contraintes : ",constraints)
    cls = clauses(tiles, constraints)
    #print(tiles)
    with open("output.cnf", "w") as f:
        f.write("p cnf %d %d\n" % (n * n * n, len(cls)))

        # Écrire les clauses dans le fichier
        for c in cls:
            f.write(" ".join([str(r) for r in c]) + " 0\n")




#on s'en fou pour l'instant
def transform_to_3sat(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    # Identifier les lignes de spécification du problème
    problem_line_index = -1
    for i, line in enumerate(lines):
        if line.startswith('p'):
            problem_line_index = i
            break

    if problem_line_index == -1:
        print("Ligne de spécification du problème non trouvée.")
        return

    num_vars, num_clauses = map(int, lines[problem_line_index].split()[2:4])

    with open(output_file, 'w') as f:
        # Écrire la ligne de spécification du problème dans le nouveau fichier
        f.write("p cnf {} {}\n".format(num_vars + 3, num_clauses))

        # Copier les clauses existantes et les transformer en 3-SAT
        for line in lines[problem_line_index + 1:]:
            clause = list(map(int, line.split()[:-1]))
            if len(clause) <= 3:
                f.write(line)
            else:
                new_clauses = []
                while len(clause) > 3:
                    new_clause = clause[:3]
                    clause = [num_vars + 1] + clause[3:]
                    num_vars += 1
                    new_clauses.append(new_clause + [num_vars])
                new_clauses.append(clause)
                for c in new_clauses:
                    f.write(" ".join(map(str, c)) + " 0\n")


#convertir le résultat donné par le sat solveur en un résultat compréhensible 
def solve(sol):
    #enlever tout pour garder que les valeur du résultat
    sol = sol.replace("s SATISFIABLE\n", "").replace("v ", "").replace(" 0", "")
   # print("sol: ",sol,"\n")
    #Mettre la solution dans un tableau
    blocks = sol.split()
    #print("blocks:\n",blocks)
    #separe la tableau en sous tableau de taille n
    grid = [blocks[i:i+n] for i in range(0, len(blocks), n)]
    #print("grid: \n", grid)
    
    c = 0
    #grid = [[0] * n for _ in range(n)]
    for i in range(n*n):
        if(i%n==0):
            print("\n")
        for j in range(0,n):
            if int(grid[i][j]) > 0:
                #print(int(grid[i][j]))
                print("case ligne :",int(i/n),", col :",c," = ",j+1)
                c+=1
                if(c==n):
                    c= 0


if __name__ == "__main__":
    if (len(sys.argv) != 2 and len(sys.argv)!=3):
        print("usage: main.py [-h] file ")
        sys.exit(1)
        #remplie le tab des clauses
    commande = "cryptominisat5 --verb=0 output.cnf"
    resultat = subprocess.run(commande, shell=True, capture_output=True, text=True)
#Option de la ligne de commande pour faire certaine étapes
    if(len(sys.argv)==3):
        if(sys.argv[1]=="-f"):#Creer le fichier dimacs
            solve_with_file(sys.argv[2])
            print("Création du fichier output.cnf")
            sys.exit()
        if(sys.argv[1]=="-s"):#Resultat du sat solver
            solve_with_file(sys.argv[2])
            print("Création du fichier output.cnf")
            sortie = resultat.stdout
            print("Resultat du sat solver :\n",sortie)  
            sys.exit()        
        if(sys.argv[1]=="-t"):#transformer le resultat du sat solver 
            solve_with_file(sys.argv[2])
            #stocker la sortie de la commande
            sortie = resultat.stdout
            #print("Resultat du sat solver :\n",sortie)
            #decoder le resultat donné par le solveur
            print("Interpretation du résultat :\n ")
            solve(sortie)
            sys.exit()
    if(sys.argv[1]=="-h"):
        print("usage: main.py [-h] file \n\n-f pour creer le fichier DIMACS\n-s pour trouver une solution au fichier DIMACS avec le sat solver\n-t pour rendre le résultat compréhensible\nPas d'option fait toutes les étapes\n")
        sys.exit()

#CAS GÉNERAL, pas d'option (fait tout):
    solve_with_file(sys.argv[1])
    print("Création du fichier output.cnf\n")
    #stocker la sortie de la commande
    sortie = resultat.stdout
    print("Resultat du sat solver :\n",sortie)
    #decoder le resultat donné par le solveur
    print("Interpretation du résultat : ")
    solve(sortie)




#parser = argparse.ArgumentParser()
#parser.add_argument('adresse fichier',help='chemin ')
#parser.add_argument('-f','--fichier',help="création fichier DIMACS")
#parser.add_argument('-s','--solve',help="solve fichier")
#args = parser.parse_args()
#print(args)


