#!/usr/bin/python
# coding: utf8

import getopt
import sys

from HTMLParser import Lexical
import HTMLUtils


def clean_balise(lex, balise):
    param_list = HTMLUtils.extract_parameters_from_html(balise.representation)
    attributs = ['type', 'data-bbox', 'data-xpath', 'data-style', 'data-area']
    new_balise = ""
    if lex.estBaliseFermante(balise):
        new_balise += '</'
    else:
        new_balise += '<'
    for param in param_list:
        if attributs.__contains__(param[0]):
            if param[0] != 'type':
                new_balise += ' ' + param[0] + '="' + param[1] + '"'
            else:
                new_balise += param[1]
    new_balise += '>'
    return new_balise


##############################################
# clean_html(inputfile, clean_list) -> str : #
##############################################
# Parametres :                               #
#  - inputfile : le fichier HTML a nettoyer  #
#  - clean_list : la liste blanche des       #
#    balises HTML a garder                   #
##############################################
# Renvoie le nouvel HTML nettoye dans un str #
##############################################
def clean_html(inputfile, clean_list):
    html_balise_unique = ['!DOCTYPE', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'keygen', 'link', 'meta', 'param', 'source', 'track', 'wbr']
    html_output = ''
    stack = []
    lex = Lexical(inputfile)
    res = lex.suivant()
    while not lex.estEOF(res):
        param_list = HTMLUtils.extract_parameters_from_html(res.representation)
        if lex.estBaliseOuvrante(res):
            if not html_balise_unique.__contains__(param_list[0][1]):
                stack.append(param_list[0][1])
        type_to_check = ''
        if len(stack) > 0:
            type_to_check = stack[len(stack) - 1]
        if len(clean_list) > 0 and clean_list.__contains__(type_to_check):
            if lex.estBaliseOuvrante(res) or lex.estBaliseFermante(res):
                if param_list[0][1] == type_to_check:
                    html_output += clean_balise(lex, res) + "\n"
            else:
                if not lex.estCommentaire(res):
                    html_output += res.representation + "\n"
        if lex.estBaliseFermante(res):
            stack.pop()
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
        print('args length :' + str(len(sys.argv)))
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
        elif opt in ("-l", "--clist"):
            clean_list = HTMLUtils.str_to_list(arg, ',')
    if inputfile != '':
        html_output = clean_html(inputfile, clean_list)
    if outputfile != '':
        fd = open(outputfile, 'w', encoding="utf-8")
        fd.write(html_output)
        print("HTML file '"+ inputfile +"' cleaned into '" + outputfile + "' !")
    else:
        print(html_output)


if __name__ == "__main__":
    main(sys.argv[1:])
