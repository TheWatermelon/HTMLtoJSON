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


def clean_html(inputfile) -> str:
    html_output = ''
    stack = []
    lex = Lexical(inputfile)
    res = lex.suivant()
    while res.type != Jeton.TYPE_EOF:
        if res.type == Jeton.TYPE_BALISE_OUVRANTE or res.type == Jeton.TYPE_CONTENU:
            stack.append(res)
        if res.type == Jeton.TYPE_BALISE_FERMANTE:
            jeton1 = stack.pop()
            if jeton1.type == Jeton.TYPE_CONTENU:
                jeton2 = stack.pop()
                balise = jeton2.representation + jeton1.representation + res.representation
            else:
                balise = jeton1.representation + res.representation
            html_output+=balise+'\n'
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

