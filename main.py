#!/usr/bin/python
# coding: utf8

import os
import sys
import getopt
import HTMLUtils
import HTMLCleaner
import HTMLtoDOM
import DOMtoJSON
import n_gramms_generator

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
        input_filename_tuple = inputfile.partition('.html')
        # prepare l'appel a HTMLCleaner
        clean_filename = input_filename_tuple[0] + "_clean.html"
        if len(clean_list) == 0:
            clean_list = ['html', 'head', 'title', 'body', 'p', 'a', 'span']
        clean_args = ""
        for value in clean_list:
            clean_args += value + ','
        subscript_argv = ['-i', inputfile, '-l', clean_args, '-o', clean_filename]
        HTMLCleaner.main(subscript_argv)
        # prepare l'appel a HTMLtoDOM
        xml_filename = input_filename_tuple[0] + "_dom.xml"
        subscript_argv = ['-i', clean_filename, '-o', xml_filename]
        HTMLtoDOM.main(subscript_argv)
        if outputfile == '':
            outputfile = input_filename_tuple[0] + ".json"
        subscript_argv = ['-i', xml_filename, '-o', outputfile]
        DOMtoJSON.main(subscript_argv)
        subscript_argv = ['-i', outputfile, '-o', outputfile]
        n_gramms_generator.main(subscript_argv)
        print('deleting temporary files... ', end="")
        os.remove(clean_filename)
        os.remove(xml_filename)
        print('done')

if __name__ == "__main__":
    main(sys.argv[1:])
