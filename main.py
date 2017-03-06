#!/usr/bin/python

import os
import sys
import getopt
import HTMLUtils

def main(argv):
    inputfile = ''
    outputfile = ''
    json_output = ''
    clean_list = []
    usage = 'usage: main.py -i <input HTML file> [-l <HTML element to keep 1>,<HTML element to keep 2>,...] [-o <output JSON file>]'
    try:
        opts, args = getopt.getopt(argv, "hi:l:o:", ["ifile=", "clist=", "ofile="])
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
        elif opt in ("-l", "--clist"):
            clean_list = HTMLUtils.str_to_list(arg, ',')
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    if inputfile != '':
        # recupere le prefixe du fichier html
        input_filename_tuple = inputfile.partition('.')
        # prepare l'appel a HTMLCleaner
        clean_filename = input_filename_tuple[0] + "_clean.html"
        if len(clean_list) == 0:
            clean_list = ['html', 'head', 'title', 'body', 'p', 'a', 'span']
        clean_args = ""
        for value in clean_list:
            clean_args += value + ','
        os.system("python HTMLCleaner.py -i " + inputfile + " -l " + clean_args + " -o " + clean_filename)
        # prepare l'appel a HTMLtoDOM
        xml_filename = input_filename_tuple[0] + "_dom.xml"
        os.system("python HTMLtoDOM.py -i " + clean_filename + " -o " + xml_filename)
        if outputfile == '':
            outputfile = input_filename_tuple[0] + ".json"
        os.system("python DOMtoJSON.py -i " + xml_filename + " -o " + outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
