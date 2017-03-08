#!/usr/bin/python

import sys
import getopt
import json

import HTMLUtils




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
    liste_balises = HTMLUtils.get_html_balises(inputfile)
    # parcours des balises
    for balise in liste_balises:
        # genere un element JSON a partir de la balise
        element = HTMLUtils.html_line_to_json_element(balise, white_list)
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
            white_list = HTMLUtils.str_to_list(arg, ',')
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
