#!/usr/bin/python

import sys
import getopt
import json

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


###########################################
# get_html_balises(inputfile) -> list :   #
###########################################
# Parametres :                            #
#  - inputfile : le fichier source        #
###########################################
# Renvoie une liste des balises contenues #
# dans le fichier source                  #
###########################################
def get_html_balises(inputfile) -> list:
    liste = []
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
            liste.append(balise)
        res = lex.suivant()
    return liste


#################################################
# extract_content_from_html_line(line) -> str : #
#################################################
# Parametres :                                  #
#  - line : une ligne composee d'une balise     #
#    ouvrante, d'un contenu et d'une balise     #
#    fermante                                   #
#################################################
# Renvoie le contenu qui se trouve entre les    #
# deux balises                                  #
#################################################
def extract_content_from_html_line(line) -> str:
    balise = False
    in_content = False
    content = ''
    for char in line:
        if char == '<':
            balise = True
            in_content = False
        elif char == '>':
            balise = False
        else:
            if not balise:
                in_content = True
        if in_content:
            content += char
    return content


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


#############################################
# html_line_to_json_element(line) -> dict : #
#############################################
# Parametres :                              #
#  - line : la ligne html a traiter         #
#  - white_list : balises autorisees        #
#############################################
# Renvoie un element JSON a partir de line  #
#############################################
def html_line_to_json_element(line, white_list) -> dict:
    element = {}
    if line[-1:] == '\n':
        line = line[:-1]
    if line != '':
        params = extract_parameters_from_html(line)
        params.append(('data', extract_content_from_html_line(line)))
        params.append(('dataHTML', line))
        for value in params:
            # checks whether the type is in the white list
            if value[0] == 'type':
                if len(white_list) > 0 and white_list.__contains__(value[1]) == False:
                   return {}
            # key => value[0], value => value[1]
            element[value[0]] = value[1]
        if element.__contains__('data-area'):
            return element
    return {}


######################################
# parse_html(inputfile) -> dict :    #
######################################
# Parametres :                       #
#  - inputfile : fichier HTML source #
#  - white_list : balises autorisees #
######################################
# Renvoie le JSON correspondant au   #
# decoupage de la page html en ne    #
# selectionnant que les balises qui  #
# sont dans la liste blanche         #
######################################
def parse_html(inputfile, white_list) -> dict:
    json_output = {'id': inputfile}
    element_list = []
    # recupere une liste de balises depuis un fichier html
    liste_balises = get_html_balises(inputfile)
    # parcours des balises
    for balise in liste_balises:
        # genere un element JSON a partir de la balise
        element = html_line_to_json_element(balise, white_list)
        # si l'element est non vide
        if len(element) > 0:
            element_list.append(element)
    # tri des elements par leur cle 'data-area'
    sorted_element_list = sorted(element_list, key=lambda k: k['data-area'])
    json_output['nb_elements'] = len(sorted_element_list)
    json_output['elements'] = sorted_element_list
    return json_output


def main(argv):
    json_output = {}
    inputfile = ''
    outputfile = ''
    white_list = []
    usage = 'usage: HTMLtoJSON.py -i <input HTML file> [-l <HTML element>,...] [-o <output JSON file>]'
    try:
        opts, args = getopt.getopt(argv, "hi:l:o:", ["ifile=", "wlist=", "ofile="])
    except getopt.GetoptError:
        print('args length :'+str(len(sys.argv)))
        print(usage)
        sys.exit(2)
    if len(sys.argv) < 3:
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
            white_list = str_to_list(arg, ',')
    if inputfile != '':
        json_output = parse_html(inputfile, white_list)
    if outputfile != '':
        fd = open(outputfile, 'w')
        fd.write(json.dumps(json_output, indent=4))
        print("JSON file created!")
    else:
        print(json.dumps(json_output, indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
