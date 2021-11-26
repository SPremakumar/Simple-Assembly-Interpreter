#! /usr/bin/env python3
# -*- coding: utf-8 -*-

#*******************************************************
# Nom.........: operation.py
# Rôle........: Pour faire tourner l'ordinateur en papier
# Version.....: V2 du 19/05/2020
# Licence.....: réalisé dans le cadre du cours de d'architecture de l'ordinateur
# Usgae - Avant : chmod 756 operation.py assembly_interpreter.py
# Usage  - Pour exécuter : python assembly_interpreter.py fichier.txt
#********************************************************/


import numpy as np
import pandas as pd

# La mémoire
memoire = [0] * 256 
a = [0] * 1


# Lecture de la mémoire 
def lire_mem(mem):
    num = np.array(mem)
    reshaped = num.reshape(16,16)
    row = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    table = pd.DataFrame(reshaped,index=row,columns=row)
    print(table)

# Ecriture dans la mémoire
def ecrire_mem(mem, hexacode, content):
    content = ['0x{}'.format(i).lower() for i in content]
    mem[hexacode] = content      
            
# Pour faire un pointeur 
def pointeur(mem, case) :
    out = mem[case] 
    
    if type(out) is str :
        out = int(out, base=16) # Convertir le str() en int()
    elif type(out) is int : 
        out = int(out)
        
    pointeur = mem[out]
    return pointeur

# Les instructions
# Adressage immédiat = I
def load_I(lst, content): # 00
    lst[0] = content # Charge le contenu dans le registre A     
    
def nand_I(lst, value): # 22
    a = int(lst[0])
    res = not(a & value)
    lst[0] = int(res)
    return lst

def add_I(lst, value): # 20
    a = lst[0]
    res = int(a) + int(value)
    lst[0] = res
    return lst

def sub_I(lst, value): # 21
    a = lst[0]
    res = int(a) - int(value)
    lst[0] = res
    return lst

# Adressage direct/absolu = A      
def load_A(lst, mem, value): # 40
    res = mem[value]
    lst[0] = res
    return lst # EFFACE

def add_A(lst, mem, value): # 60  
    res = mem[value] ; x = lst[0]
    add = int(res) + int(x)
    lst[0] = add
    return lst

def sub_A(lst, mem, value): # 61 
    res = mem[value] ; x = lst[0]
    sub  =  int(x) - int(res)
    lst[0] = sub
    return lst

def nand_A(lst, mem, case): # 62 
    value = mem[case] ; lst = a[0]
    res = not(int(value) & int(lst))
    return int(res)

def store_A(lst, mem, value): # 48
    to_store = lst[0]
    mem[value] = to_store
    
def in_A(mem, hexacode): # 49
    content = input('?> ')
    mem[hexacode] = content
    
def out_A(mem, hexacode): # 41
    out = mem[hexacode]
    print(out)


# Adressage indirect = IDT
def add_IDT(a, mem, case) : # E0
    x = a[0] ; pt = pointeur(mem, case)
    res = int(pt, base=16) + int(x, base=16)
    a[0] = res
    return a

def sub_IDT(a, mem, case) : # E1
    x = a[0] ; pt = pointeur(mem, case)
    res = int(pt, base=16) - int(x, base=16)
    a[0] = res
    return a

def load_IDT(a, mem, case): # C0
    pt = pointeur(mem, case)
    a[0] = pt
    return a

def nand_IDT(a, mem, case): # E2
    pt = pointeur(mem, case); lst = a[0]
    res = not(int(lst) & int(pt))
    a[0] = int(res)
    return a

def store_IDT(a, mem, case): # C8
    x = a[0] ; out = mem[case]
    out = int(out)
    mem[out] = x

def in_IDT(mem, case): # C9
    pt = pointeur(mem, case) ; pt = int(pt)
    content = input('?> ')
    mem[pt] = content

def out_IDT(mem, case): # C1
    pt = pointeur(mem, case); pt = int(pt)
    return pt

table_op = {
 '0x20' : ['add #', 'A + _'],   
 '0x60' : ['add', 'A + (_)'],
 '0xe0' : ['add *', 'A + *(_)'],
 '0x21' : ['sub #', 'A - _'],
 '0x61' : ['sub', 'A - (_)'],
 '0xe1' : ['sub *', 'A - *(_)'],
 '0x22' : ['nand #', '~[A & _]'],
 '0x62' : ['nand', '~[A & (_)]'],
 '0xe2' : ['nand *', '~[A & *(_)]'],
 '0x00' : ['load #', 'A <= _'],
 '0x40' : ['load', 'A <= (_)'],
 '0xc0' : ['load *', 'A <= *(_)'],
 '0x48' : ['store', '(_) <= A'],
 '0xc8' : ['store *', '*(_) <= A'],
 '0x49' : ['in', 'ENTREE'],
 '0xc9' : ['in *', 'ENTREE*'],
 '0x41' : ['out', 'SORTIE'],
 '0xc1' : ['out *', 'SORTIE'],
 '0x10' : ['jump', 'PC = _'], 
 '0x11' : ['brn', 'if A < 0 : PC = _'],
 '0x12' : ['brz', 'if not A : PC = _'], 
    }

def execute(mem=memoire, a=a):
    pc = 0
    
    while pc < len(mem):
        x = mem[pc]
        pc += 1 
        
        if type(x) is list :
            opc = x[0]
            if x[1] == '0x_' : # Quand la valeur est vide
            	x[1] = '0'   
            value = int(x[1], base=16)
            print('PC : %s | A : %s | %s \t| %s \t' %(str(hex(pc-1)), a[0], table_op[opc][0], table_op[opc][1].replace('_',str(hex(value)))))  
            
            if opc == '0x60' :
                add_A(a, mem, value)
            elif opc == '0x61' :
                sub_A(a, mem, value)
            elif opc == '0x62' : 
                nand_A(a, mem, value)            
            elif opc == '0x40' : 
                load_A(a, mem, value)                  
            elif opc == '0x48' : 
                store_A(a, mem, value)
            elif opc == '0x49' :
                in_A(mem, value)
            elif opc == '0x41' :
                out_A(mem, value)
                
            elif opc == '0x20' :
                add_I(a, value)
            elif opc == '0x21' :
                sub_I(a, value)
            elif opc == '0x22' :
                nand_I(a, value)
            elif opc == '0x00' :
                load_I(a, value)     
            
            elif opc == '0xe0' :
                add_IDT(a, mem, value)
            elif opc == '0xe1' :
                sub_IDT(a, mem, value)
            elif opc == '0xe1' :
                nand_IDT(a, mem, value)
            elif opc == '0xc0' :
                load_IDT(a, mem, value)
            elif opc == '0xc8' :
                store_IDT(a, mem, value)
            elif opc == '0xc9' :
                in_IDT(mem, value)
            elif opc == '0xc1' :
                out_IDT(mem, value)
            
            elif opc == '0x10' :
                pc = value
            elif opc == '0x11' :
                if a[0] < 0 :
                    pc = value 
            elif opc == '0x12' :
                if a[0] == 0 : 
                    pc = value 
