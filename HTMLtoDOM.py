#!/usr/bin/python

import sys
import getopt
import HTMLUtils
import xml.dom.minidom

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
        fd = open(inputfile, 'r', encoding="utf8")

        buffer = ""
        for line in fd.readlines():
            for char in line:
                # DEBUG : ajout du caractere '&' dans les caracteres interdits
                if char != '\t' and char != '\n' and char != '\r' and char != '&':
                    buffer += char

        dom = xml.dom.minidom.parseString(buffer)
        xml_output = dom.toprettyxml()
    if outputfile != '':
        fd = open(outputfile, 'w', encoding="utf8")
        fd.write(xml_output)
        print("DOM of '" + inputfile + "' generated into '" + outputfile + "' !")
    else:
        print(xml_output)


if __name__ == "__main__":
    main(sys.argv[1:])
