#!/usr/bin/python

####################################################
#                       Jeton                      #
####################################################
# Cette classe represente un jeton lexical.        #
####################################################
# Attributs :                                      #
#  - type : entier qui represente le type du jeton #
#    (balise ouvrante, fermante, contenu           #
#     ou fin de fichier)                           #
#  - representation : le contenu du jeton (str)    #
####################################################
class Jeton:
    TYPE_BALISE_OUVRANTE = 0
    TYPE_BALISE_FERMANTE = 1
    TYPE_CONTENU = 2
    TYPE_COMMENTAIRE = 3
    TYPE_EOF = -1

    def __init__(self, type_jeton, representation):
        self.type = type_jeton
        self.representation = representation

    def print(self):
        print('[' + str(self.type) + ': ' + self.representation + ']')


###########################################
#                 Lexical                 #
###########################################
# Cette classe est une analyseur lexical. #
###########################################
# Attributs :                             #
#  - inputfile : le fichier source        #
#  - ligne : une ligne du fichier         #
#  - position : un curseur sur la ligne   #
###########################################
# Methodes :                              #
#  - avance() -> bool : avance le curseur #
#    sur la ligne, charge une nouvelle    #
#    ligne lorsque le curseur depasse     #
#  - suivant() -> Jeton : renvoie le      #
#    prochain jeton de la ligne courante  #
###########################################
class Lexical:
    def __init__(self, filename):
        self.inputfile = open(filename, encoding="utf8")
        self.ligne = self.inputfile.readline(1000000)
        self.position = 0

    def avance(self) -> bool:
        if self.ligne == '':
            return False
        if self.position == len(self.ligne):
            self.ligne = self.inputfile.readline(1000000)
            if self.ligne == '':
                return False
            self.position = 0
            self.avance()
        c = self.ligne[self.position]
        # passer les espaces
        if not (c == ' ' or c == '\t' or c == '\r' or c == '\n'):
            return True
        self.position += 1
        return self.avance()

    def suivant(self) -> Jeton:
        if not (self.avance()):
            return Jeton(Jeton.TYPE_EOF, "")
        c = self.ligne[self.position]
        if c == '<':
            buffer = ''
            # commentaire HTML
            if self.ligne[self.position+1] == '!' and \
                self.ligne[self.position+2] == '-' and \
                self.ligne[self.position+3] == '-':
                while self.ligne[self.position] != '-' or \
                        self.ligne[self.position+1] != '-' or \
                        self.ligne[self.position+2] != '>':
                    buffer += c
                    self.position += 1
                    if self.position == len(self.ligne):
                        if not (self.avance()):
                            return Jeton(Jeton.TYPE_EOF, "")
                    c = self.ligne[self.position]
                buffer += self.ligne[self.position] + self.ligne[self.position+1] + self.ligne[self.position+2]
                self.position += 3
                c = self.ligne[self.position]
                return Jeton(Jeton.TYPE_COMMENTAIRE, buffer)
            # balise classique
            else:
                while c != '>':
                    buffer += c
                    self.position += 1
                    if self.position == len(self.ligne):
                        if not (self.avance()):
                            return Jeton(Jeton.TYPE_EOF, "")
                    c = self.ligne[self.position]
                buffer += c
                self.position += 1
                if buffer[1] == '/':
                    return Jeton(Jeton.TYPE_BALISE_FERMANTE, buffer)
                else:
                    return Jeton(Jeton.TYPE_BALISE_OUVRANTE, buffer)
        else:
            buffer = ''
            while c != '<':
                buffer += c
                self.position += 1
                if self.position == len(self.ligne):
                    if not (self.avance()):
                        return Jeton(Jeton.TYPE_EOF, "")
                c = self.ligne[self.position]
            return Jeton(Jeton.TYPE_CONTENU, buffer)

    def estBaliseOuvrante(self, jeton) -> bool:
        return jeton.type == Jeton.TYPE_BALISE_OUVRANTE

    def estBaliseFermante(self, jeton) -> bool:
        return jeton.type == Jeton.TYPE_BALISE_FERMANTE

    def estContenu(self, jeton) -> bool:
        return jeton.type == Jeton.TYPE_CONTENU

    def estCommentaire(self, jeton) -> bool:
        return jeton.type == Jeton.TYPE_COMMENTAIRE

    def estEOF(self, jeton) -> bool:
        return jeton.type == Jeton.TYPE_EOF


