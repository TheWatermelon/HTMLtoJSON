#!/usr/bin/python
# coding: utf8

import sys
import getopt
from xml.dom import minidom
from xml.parsers.expat import ExpatError
import HTMLUtils
from HTMLLexer import Lexical


def main(argv):
    inputfile = ''
    outputfile = ''
    xml_output = ''
    usage = 'usage: HTMLtoDOM.py -i <input HTML file> [-o <output XML file>]'
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
        lex = Lexical(inputfile)
        res = lex.suivant()
        buffer = ""
        while not lex.estEOF(res):
            entity = False
            entity_code = ""
            if not lex.estContenu(res):
                buffer += res.representation
            else:
                for char in res.representation:
                    if not entity:
                        if char != '\t' and char != '\n' and char != '\r' and char != '&':
                            buffer += char
                        elif char == '&':
                            entity = True
                            entity_code += char
                    else:
                        if char != ';':
                            entity_code += char
                        else:
                            entity_code += char
                            if HTMLUtils.xml_entities.__contains__(entity_code):
                                buffer += entity_code
                            elif HTMLUtils.html_entities.keys().__contains__(entity_code):
                                buffer += HTMLUtils.html_entities[entity_code]
                            entity_code = ""
                            entity = False
            res = lex.suivant()
        try:
            dom = minidom.parseString(buffer)
            xml_output = dom.toprettyxml()
        except ExpatError:
            print(ExpatError)
    if outputfile != '':
        fd = open(outputfile, 'w', encoding="utf-8")
        fd.write(xml_output)
        print("DOM of '" + inputfile + "' generated into '" + outputfile + "' !")
    else:
        print(xml_output)


if __name__ == "__main__":
    main(sys.argv[1:])
