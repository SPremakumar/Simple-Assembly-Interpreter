#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#*******************************************************
# Nom.........: assembly_interpreter.py
# Rôle........: Pour faire tourner l'ordinateur en papier
# Auteur......: Samya PREMAKUMAR
# Version.....: V2 du 19/05/2020
# Licence.....: réalisé dans le cadre du cours de d'architecture de l'ordinateur
# Usgae - Avant : chmod 756 operation.py assembly_interpreter.py
# Usage  - Pour exécuter : python assembly_interpreter.py fichier.txt
#********************************************************/


import operation as op
import sys

# La mémoire
memoire = [0] * 256 
a = [0] * 1

# Ecrire les instructions du fichier 'filename' dans la memoire
def write_file_to_mem(filename, memoire=memoire):
    with open(filename, mode='r') as f:
        content = f.read().splitlines()
    
    for value in content :
        value = value.split('#', 1)[0] # Les commentaires
        value = value.split() 
        ad_d = int(value[0], base=16)
        code_mem = value[1:]
        op.ecrire_mem(memoire, ad_d, code_mem) # Ecrire les instructions dans la mémoire 

    op.execute(memoire)
    print(" ")
    op.lire_mem(memoire)

try : 
	if len(sys.argv) == 1 : 
		exit("Argument manquant")
	else : 
		write_file_to_mem(sys.argv[1])
except KeyboardInterrupt :
		print("Vous avez quitter le programme")
		print(" ")
		print(memoire)
except ImportError : 
		print("Erreur -01: pas de module")
except IOError :
	print("Erreur 00 : Le fichier entré n'existe pas ou/et est mal orthographié ou/et n'a pas les autorisations pour être éxecuter ")
except TypeError : 
		print("Erreur 01 : Vous essayez de faire rentrer une instruction dans l'Acc (du type [00 00])")
except NameError :
		print("Erreur 02 : Vous devez rentrer un nombre")
except SyntaxError : 
		print("Erreur 03 : Vous avez rajouter un element inconnue (lettre, ?,', §, !, ...) à un nombre")
except IndexError :
		print("Erreur 04 : le fichier entré comporte une (des) erreur(s)")