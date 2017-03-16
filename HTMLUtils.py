#!/usr/bin/python
# coding: utf8

from HTMLLexer import Lexical

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


############################################
# str_to_list(string, delimiter) -> list : #
############################################
# Parametres :                             #
#   - string : la chaine a decouper        #
#   - delimiter : le delimiteur            #
############################################
# Renvoie une liste de tous les elements   #
# separes par le delimiteur dans la chaine #
############################################
def str_to_list(string, delimiter):
    liste = []
    tuple_part = string.partition(delimiter)
    # cas string avec delimiter
    while tuple_part[1] != '':
        liste.append(tuple_part[0])
        tuple_part = tuple_part[2].partition(delimiter)
    # cas string sans delimiter
    if tuple_part[1] == '' and tuple_part[0] != '':
        liste.append(tuple_part[0])
    return liste


###########################################
# get_html_balises(inputfile) -> list :   #
###########################################
# Parametres :                            #
#  - inputfile : le fichier source        #
###########################################
# Renvoie une liste des balises contenues #
# dans le fichier source                  #
###########################################
def get_html_balises(inputfile):
    liste = []
    stack = []
    lex = Lexical(inputfile)
    res = lex.suivant()
    while not lex.estEOF(res):
        if lex.estBaliseOuvrante(res) or lex.estContenu(res):
            stack.append(res)
        if lex.estBaliseFermante(res):
            jeton1 = stack.pop()
            if lex.estContenu(jeton1):
                jeton2 = stack.pop()
                balise = jeton2.representation + jeton1.representation + res.representation
            else:
                balise = jeton1.representation + res.representation
            liste.append(balise)
        res = lex.suivant()
    return liste


#################################################
# extract_content_from_html_line(line) -> str : #
#################################################
# Parametres :                                  #
#  - line : une ligne composee d'une balise     #
#    ouvrante, d'un contenu et d'une balise     #
#    fermante                                   #
#################################################
# Renvoie le contenu qui se trouve entre les    #
# deux balises                                  #
#################################################
def extract_content_from_html_line(line):
    balise = False
    in_content = False
    content = ''
    for char in line:
        if char == '<':
            balise = True
            in_content = False
        elif char == '>':
            balise = False
        else:
            if not balise:
                in_content = True
        if in_content:
            content += char
    return content


################################################
# extract_parameters_from_html(line) -> list : #
################################################
# Parametres :                                 #
#  - balise : la balise ouvrante html          #
################################################
# Renvoie la liste des parametres plus le type #
# de la balise                                 #
################################################
def extract_parameters_from_html(balise):
    param_liste = []
    type_balise = True
    type_content = ''
    key = False
    key_content = ''
    value = False
    value_content = ''
    for char in balise:
        if char == ' ' or char == '>':
            if type_balise:
                type_balise = False
                param_liste.append(('type', type_content))
            if not value:
                key = True
            else:
                value_content += ' '
            if key_content != '' and value_content != '' and not value:
                param_liste.append((key_content, value_content))
                key_content = ''
                value_content = ''
            continue
        if char == '"':
            value = not value
            continue
        if type_balise:
            if char != '<' and char != '/':
                type_content += char
        if value:
            value_content += char
        if key:
            if char == '=':
                key = False
            else:
                key_content += char
    return param_liste


#############################################
# html_line_to_json_element(line) -> dict : #
#############################################
# Parametres :                              #
#  - line : la ligne html a traiter         #
#  - white_list : balises autorisees        #
#############################################
# Renvoie un element JSON a partir de line  #
#############################################
def html_line_to_json_element(line, white_list):
    element = {}
    if line[-1:] == '\n':
        line = line[:-1]
    if line != '':
        params = extract_parameters_from_html(line)
        params.append(('data', extract_content_from_html_line(line)))
        params.append(('dataHTML', line))
        for value in params:
            # checks whether the type is in the white list
            if value[0] == 'type':
                if len(white_list) > 0 and white_list.__contains__(value[1]) == False:
                   return {}
            # key => value[0], value => value[1]
            element[value[0]] = value[1]
        if element.__contains__('data-area'):
            return element
    return {}

