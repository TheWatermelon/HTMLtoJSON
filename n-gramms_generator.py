#!/usr/bin/python

import sys
import getopt
import json

import HTMLUtils


def add_n_gramm_to_list(n_gramm_list, new_n_gramm, ponctuation):
    n_gramm_list.append(new_n_gramm)
    for n_gramm in n_gramm_list:
        if n_gramm[0] == new_n_gramm[0] - 1:
            n_gramm_list.append((new_n_gramm[0], n_gramm[1] + 1, n_gramm[2] + ponctuation + new_n_gramm[2]))


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
def generate_ngramms(inputfile) -> dict:
    ponc_faible = [' ', '-', '\'']
    ponc_forte = ['.', ',', ';', '\n']

    json_input = json.load(open(inputfile, 'r', encoding="utf8"))
    json_output = {'nb_blocks': json_input['nb_blocks']}

    for block in json_input['blocks']:
        text = block['text']
        all_n_gramms = []
        current_n_gramms = []
        buffer = ""
        ponctuation = ""
        index = 0
        for char in text:
            if not ponc_faible.__contains__(char) \
                    and not ponc_forte.__contains__(char):
                if char != '\n' and char != '\t':
                    buffer += char
            else:
                if buffer != "":
                    add_n_gramm_to_list(current_n_gramms, (index, 1, buffer), ponctuation)
                ponctuation = char
                buffer = ""
                index += 1
                if ponc_forte.__contains__(char):
                    if len(current_n_gramms) > 0:
                        all_n_gramms.append(current_n_gramms)
                        current_n_gramms = []
        # cas ou le texte ne contient pas de ponctuation forte
        if len(current_n_gramms) > 0:
            if buffer != "":
                add_n_gramm_to_list(current_n_gramms, (index, 1, buffer), ponctuation)
            all_n_gramms.append(current_n_gramms)
        # cas ou le texte ne contient qu'un mot
        else:
            all_n_gramms.append([(0, 1, buffer)])
        output_block = { 'id': block['id'], 'text': text, 'n-gramms': all_n_gramms }
        json_output[block['id']] = output_block
    return json_output


def main(argv):
    json_output = {}
    inputfile = ''
    outputfile = ''
    usage = 'usage: n-gramms_generator.py -i <input JSON file> [-o <output JSON file>]'
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('args length :' + str(len(sys.argv)))
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
    if inputfile != '':
        json_output = generate_ngramms(inputfile)
    if outputfile != '':
        fd = open(outputfile, 'w')
        fd.write(json.dumps(json_output, indent=4))
        print("JSON file created!")
    else:
        print(json.dumps(json_output, indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
