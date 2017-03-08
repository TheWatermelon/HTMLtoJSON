#!/usr/bin/python

import sys
import getopt
import json

import HTMLUtils


##################################################################
# add_n_gramm_to_list(n_gramms_list, new_n_gramm, ponctuation) : #
##################################################################
# Parametres :                                                   #
#  - n_gramms_list : la liste dans laquelle ajouter le n-gramme  #
#  - new_n_gramm : le n-gramme a ajouter                         #
#  - ponctuation : la ponctuation entre le nouveau n-gramme et   #
#    les n-grammes qui lui sont lies (les n-grammes qui le       #
#    precede                                                     #
##################################################################
# Ne renvoie rien                                                #
##################################################################
def add_n_gramm_to_list(n_gramms_list, new_n_gramm, ponctuation):
    n_gramms_list.append(new_n_gramm)
    for n_gramm in n_gramms_list:
        if n_gramm[0] == new_n_gramm[0] - 1:
            n_gramms_list.append((new_n_gramm[0], n_gramm[1] + 1, n_gramm[2] + ponctuation + new_n_gramm[2]))


#########################################
# generate_ngramms(inputfile) -> dict : #
#########################################
# Parametres :                          #
#  - inputfile : fichier JSON source    #
#########################################
# Renvoie le JSON correspondant au      #
# decoupage en n-grammes des blocs de   #
# texte                                 #
#########################################
def generate_ngramms(inputfile) -> dict:
    ponc_faible = [' ', '-', '\'']
    ponc_forte = ['.', ',', ';', '\n']

    json_output = json.load(open(inputfile, 'r', encoding="utf8"))

    for block in json_output['blocks']:
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
                # ajout de la ponctuation faible comme n-gramme
                if ponc_faible.__contains__(char) and char != ' ':
                    add_n_gramm_to_list(current_n_gramms, (index, 1, buffer), ponctuation)
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
        # construction du block avec ses n-grammes
        output_block = {}
        for key,value in block.items():
            output_block[key] = value
        new_list = []
        for n_gramms_list in all_n_gramms:
            for item in n_gramms_list:
                n_gramm = {'size': item[1], 'n_gramms': item[2]}
                new_list.append(n_gramm)
        block['n_grammes'] = new_list
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
        print("n-grammes generated into '" + outputfile + "' !")
    else:
        print(json.dumps(json_output, indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
