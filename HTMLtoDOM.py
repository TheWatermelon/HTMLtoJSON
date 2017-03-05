#!/usr/bin/python

import sys
import getopt
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

        xml_entities = ['&quot;', '&amp', '&apos;', '&lt;', '&gt;']
        html_entities = { '&quot;': '\"',
                          '&amp;': '&',
                          '&apos;': '\'',
                          '&lt;': '<',
                          '&gt;': '>',
                          '&nbsp;': ' ',
                          '&iexcl;': '¡',
                          '&cent;': '¢',
                          '&pound;': '£',
                          '&curren;': '¤',
                          '&yen;': '¥',
                          '&brvbar;': '¦',
                          '&sect;': '§',
                          '&uml;': '¨',
                          '&copy;': '©',
                          '&ordf;': 'ª',
                          '&laquo;': '«',
                          '&not;': '¬',
                          '&reg;': '®',
                          '&macr;': '¯',
                          '&deg;': '°',
                          '&plusmn;': '±',
                          '&sup2;': '²',
                          '&sup3;': '³',
                          '&acute;': '´',
                          '&micro;': 'µ',
                          '&para;': '¶',
                          '&middot;': '·',
                          '&cedil;': '¸',
                          '&sup1;': '¹',
                          '&ordm;': 'º',
                          '&raquo;': '»',
                          '&frac14;': '¼',
                          '&frac12;': '½',
                          '&frac34;': '¾',
                          '&iquest;': '¿',
                          '&Agrave;': 'À',
                          '&Aacute;': 'Á',
                          '&Acirc;': 'Â',
                          '&Atilde;': 'Ã',
                          '&Auml;': 'Ä',
                          '&Aring;': 'Å',
                          '&AElig;': 'Æ',
                          '&Ccedil;': 'Ç',
                          '&Egrave;': 'È',
                          '&Eacute;': 'É',
                          '&Ecirc;': 'Ê',
                          '&Euml;': 'Ë',
                          '&Igrave;': 'Ì',
                          '&Iacute;': 'Í',
                          '&Icirc;': 'Î',
                          '&Iuml;': 'Ï',
                          '&ETH;': 'Ð',
                          '&Ntilde;': 'Ñ',
                          '&Ograve;': 'Ò',
                          '&Oacute;': 'Ó',
                          '&Ocirc;': 'Ô',
                          '&Otilde;': 'Õ',
                          '&Ouml;': 'Ö',
                          '&times;': '×',
                          '&Oslash;': 'Ø',
                          '&Ugrave;': 'Ù',
                          '&Uacute;': 'Ú',
                          '&Ucirc;': 'Û',
                          '&Uuml;': 'Ü',
                          '&Yacute;': 'Ý',
                          '&THORN;': 'Þ',
                          '&szlig;': 'ß',
                          '&agrave;': 'à',
                          '&aacute;': 'á',
                          '&acirc;': 'â',
                          '&atilde;': 'ã',
                          '&auml;': 'ä',
                          '&aring;': 'å',
                          '&aelig;': 'æ',
                          '&ccedil;': 'ç',
                          '&egrave;' : 'è',
                          '&eacute;': 'é',
                          '&ecirc;': 'ê',
                          '&euml;': 'ë',
                          '&igrave;': 'ì',
                          '&iacute;': 'í',
                          '&icirc;': 'î',
                          '&iuml;': 'ï',
                          '&eth;': 'ð',
                          '&ntilde;': 'ñ',
                          '&ograve;': 'ò',
                          '&oacute;': 'ó',
                          '&ocirc;': 'ô',
                          '&otilde;': 'õ',
                          '&ouml;': 'ö',
                          '&divide;': '÷',
                          '&oslash;': 'ø',
                          '&ugrave;': 'ù',
                          '&uacute;': 'ú',
                          '&ucirc;': 'û',
                          '&uuml;': 'ü',
                          '&yacute;': 'ý',
                          '&yuml;': 'ÿ',
                          '&OElig;': 'Œ',
                          '&oelig;': 'œ',
                          '&Yuml;': 'Ÿ',
                          '&fnof;': 'ƒ',
                          '&circ;': 'ˆ',
                          '&tilde;': '˜'
                          }

        buffer = ""
        for line in fd.readlines():
            entity = False
            entity_code = ""
            for char in line:
                if not entity:
                    # DEBUG : ajout du caractere '&' dans les caracteres interdits
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
                        if xml_entities.__contains__(entity_code):
                            buffer += entity_code
                        elif html_entities.keys().__contains__(entity_code):
                            buffer += html_entities[entity_code]
                        entity_code = ""
                        entity = False



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
