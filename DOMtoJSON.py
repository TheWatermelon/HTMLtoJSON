#!/usr/bin/python

import sys
import json
import getopt
import HTMLUtils
import xml.etree.ElementTree as ET

def dom_to_json(inputfile) -> dict:
    json_output = {}
    blocks = []
    nb_blocks = 0
    tree = ET.parse(inputfile)
    for element in tree.iter():
        buffer = ""
        for text in element.itertext():
            for char in text:
                if char != '\t' and char != '\n':
                    buffer += char
        if not buffer.isspace():
            bloc = {'id':nb_blocks, 'text':buffer}
            blocks.append(bloc)
            nb_blocks += 1
    json_output['nb_blocks'] = nb_blocks
    json_output['blocks'] = blocks
    return json_output


def main(argv):
    inputfile = ''
    outputfile = ''
    json_output = ''
    clean_list = []
    usage = 'usage: XMLtoJSON.py -i <input XML DOM file> [-o <output JSON file>]'
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
        fd = open(outputfile, 'w', encoding="utf8")
        fd.write(json.dumps(json_output, indent=4))
        print("XML DOM file '"+ inputfile +"' changed into JSON blocks (" + outputfile + ")")
    else:
        print(json.dumps(json_output, indent=4))


if __name__ == "__main__":
    main(sys.argv[1:])