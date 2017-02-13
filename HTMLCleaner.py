#!/usr/bin/python

import getopt
import sys

from HTMLParser import Jeton
from HTMLParser import Lexical


############################################
# str_to_list(string, delimiter) -> list : #
############################################
# Parametres :                             #
#   - string : la chaine a decouper        #
#   - delimiter : le delimiteur            #
############################################
# Renvoie une liste de tous les elements   #
# separes par le delimiteur dans la chaine #
############################################
def str_to_list(string, delimiter) -> list:
    liste = []
    tuple_part = string.partition(delimiter)
    # cas string avec delimiter
    while tuple_part[1] != '':
        liste.append(tuple_part[0])
        tuple_part = tuple_part[2].partition(delimiter)
    # cas string sans delimiter
    if tuple_part[1] == '' and tuple_part[0] != '':
        liste.append(tuple_part[0])
    return liste


################################################
# extract_parameters_from_html(line) -> list : #
################################################
# Parametres :                                 #
#  - balise : la balise ouvrante html          #
################################################
# Renvoie la liste des parametres plus le type #
# de la balise                                 #
################################################
def extract_parameters_from_html(balise) -> list:
    param_liste = []
    type_balise = True
    type_content = ''
    key = False
    key_content = ''
    value = False
    value_content = ''
    for char in balise:
        if char == ' ' or char == '>':
            if type_balise:
                type_balise = False
                param_liste.append(('type', type_content))
            if not value:
                key = True
            else:
                value_content += ' '
            if key_content != '' and value_content != '' and not value:
                param_liste.append((key_content, value_content))
                key_content = ''
                value_content = ''
            continue
        if char == '"':
            value = not value
            continue
        if type_balise:
            if char != '<':
                type_content += char
        if value:
            value_content += char
        if key:
            if char == '=':
                key = False
            else:
                key_content += char
    return param_liste


def clean_html(inputfile, clean_list) -> str:
    html_output = ''
    stack = []
    lex = Lexical(inputfile)
    res = lex.suivant()
    while not lex.estEOF(res):
        param_list = extract_parameters_from_html(res.representation)
        if lex.estBaliseOuvrante(res):
            stack.append(param_list[0][1])
        type_to_check = ''
        if len(stack) > 0:
            type_to_check = stack[len(stack)-1]
        if len(clean_list) > 0 and clean_list.__contains__(type_to_check) == True:
            if len(stack) > 0 and lex.estBaliseOuvrante(res):
                for i in range(0, len(stack)-1):
                    html_output+='\t'
            html_output+=res.representation
        if lex.estBaliseFermante(res):
            stack.pop()
            html_output+='\n'
        res = lex.suivant()
    return html_output


def main(argv):
    inputfile = ''
    outputfile = ''
    html_output = ''
    clean_list = []
    usage = 'usage: HTMLCleaner.py -i <input HTML file> -l <HTML element>,... [-o <output JSON file>]'
    try:
        opts, args = getopt.getopt(argv, "hi:l:o:", ["ifile=", "clist=", "ofile="])
    except getopt.GetoptError:
        print('args length :'+str(len(sys.argv)))
        print(usage)
        sys.exit(2)
    if len(sys.argv) < 5:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-l", "--wlist"):
            clean_list = str_to_list(arg, ',')
    if inputfile != '':
        html_output = clean_html(inputfile, clean_list)
    if outputfile != '':
        fd = open(outputfile, 'w')
        fd.write(html_output)
        print("HTML file cleaned into "+outputfile+" !")
    else:
        print(html_output)


if __name__ == "__main__":
    main(sys.argv[1:])

