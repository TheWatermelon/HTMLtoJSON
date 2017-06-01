#!/usr/bin/python

import sys
import json
import getopt
import xml.etree.ElementTree as ET


#############################
# extract_tag(tag) -> str : #
#############################
# Parametres :              #
#   - tag : le tag recu de  #
#     la forme {lien}tag    #
#############################
# Renvoie le tag juste      #
# apres les {}              #
#############################
def extract_tag(tag):
    ret = tag.partition('}')
    return ret[2]


#################################
# select_style(root) -> str :   #
#################################
# Parametres :                  #
#   - root : le noeud parent    #
#     du bloc contenant les     #
#     elements textuels         #
#################################
# Renvoie le style majoritaire  #
# parmi les styles des elements #
# en se basant sur le perimetre #
# des elements                  #
#################################
def select_style(root):
    max_bbox_aire = 0
    style = ""
    for child in root.iter():
        bbox = child.attrib.get('data-bbox', '0 0 0 0')
        # retire x
        bbox_tuple = bbox.partition(' ')
        # retire y
        bbox_tuple = bbox_tuple[2].partition(' ')
        # separe width et height
        bbox_tuple = bbox_tuple[2].partition(' ')
        # calcul de l'aire
        bbox_aire = int(bbox_tuple[0]) * int(bbox_tuple[2])
        # selection du style
        if(bbox_aire > max_bbox_aire):
            max_bbox_aire = bbox_aire
            style = child.attrib.get('data-style', '')
    return style


######################################
# dom_to_json(inputfile) -> dict :   #
######################################
# Parametres :                       #
#   - inputfile : le DOM au format   #
#     XML                            #
######################################
# Renvoie le JSON correspondant      #
# a la generation des blocs textuels #
# depuis les elements du DOM         #
######################################
def dom_to_json(inputfile):
    json_output = {}
    blocks = []
    tree = ET.parse(inputfile)
    index = 0
    for child in tree.getroot().findall('*'):
        buffer = ""
        for text in child.itertext():
            if not text.isspace():
                buffer += text
        if not len(buffer) == 0:
            index += 1
            block = {}
            block['id'] = index
            block['data-xpath'] = child.attrib.get('data-xpath', '')
            block['data-area'] = child.attrib.get('data-area', '')
            block['data-style'] = select_style(child)
            block['text'] = buffer
            blocks.append(block)
                    
    json_output['nb_blocks'] = len(blocks)
    json_output['blocks'] = blocks
    return json_output


def main(argv):
    inputfile = ''
    outputfile = ''
    json_output = ''
    clean_list = []
    usage = 'usage: DOMtoJSON.py -i <input XML DOM file> [-o <output JSON file>]'
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
        json_output = dom_to_json(inputfile)
    if outputfile != '':
        fd = open(outputfile, 'w', encoding="utf-8")
        fd.write(json.dumps(json_output, indent=4))
        print("XML DOM file '"+ inputfile +"' changed to JSON blocks into '" + outputfile + "'")
    else:
        print(json.dumps(json_output, indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])
