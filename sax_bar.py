# potrebne pro SAX
from xml.sax import handler
from xml.sax import make_parser

# potrebne na razeni ...
from operator import attrgetter


# domenova trida - Slozka
class Slozka:
    def __init__(self):
        self.__id = 0
        self.__nazev = ""
        self.__cena = ""

    def getId(self):
        return self.__id

    def setId(self, idcko):
        self.__id = idcko

    def getNazev(self):
        return self.__nazev

    def setNazev(self, nazev):
        self.__nazev = nazev

    def getCena(self):
        return self.__cena

    def setCena(self, cena):
        self.__cena = cena


# domenova trida - Koktejl
class Koktejl:
    def __init__(self):
        self.__id = 0
        self.__nazev = ""
        self.__cena = 0
        self.__vydaje = 0
        self.zisk = 0

    def getId(self):
        return self.__id

    def setId(self, idcko):
        self.__id = idcko

    def getNazev(self):
        return self.__nazev;

    def setNazev(self, nazev):
        self.__nazev = nazev

    def getCena(self):
        return self.__cena

    def setCena(self, cena):
        self.__cena = cena

    def getZisk(self):
        return self.zisk

    def getVydaje(self):
        return self.__vydaje

    def spocitejZisk(self):
        self.zisk = self.__cena - self.__vydaje

    def addVydaj(self, slozky, idcko, mnozstvi):
        for slozka in slozky:
            if (slozka.getId() == idcko):
                self.__vydaje += mnozstvi * slozka.getCena()
                break

            # Definice nove tridy oddedene od ContentHandler


class BarHandler(handler.ContentHandler):

    # konstruktor tridy    
    def __init__(self):

        # inicializace dat tridy
        self.__inSlozky = False  # indikator stavu
        self.__inKoktejly = False  # indikator stavu
        self.__inNazev = False  # indikator stavu
        self.__inCena = False  # indikator stavu
        self.__inSlozka = False  # indikator stavu
        self.__koktejly = []  # seznam koktejlu
        self.__slozky = []  # seznam slozek

    # getter pro seznam koktejlu
    def getKoktejlyList(self):
        return self.__koktejly

    # prekryti metody startElement(self)
    def startElement(self, name, attrs):
        # ulozeni stavu, kde se prave ve XML nachazime
        if (name == "slozky") and (not self.__inKoktejly):
            self.__inSlozky = True
        elif (name == "koktejly"):
            self.__inKoktejly = True
        elif (name == "nazev"):
            self.__inNazev = True
        elif (name == "cena"):
            self.__inCena = True
        elif (name == "slozka"):
            self.__inSlozka = True
            if self.__inSlozky:
                # vytvoreni instance slozky (jsme uvnitr slozky, ne v koktejlu)
                self.__slozka = Slozka()
                self.__slozka.setId(int(attrs.get("id")))
            else:
                self.__id = int(attrs.get("id"))
        elif (name == "koktejl"):
            # vytvoreni instance koktejlu
            self.__koktejl = Koktejl()
            self.__koktejl.setId(int(attrs.get("id")))

    # prekryti metody endElement(self, name)
    def endElement(self, name):
        # ulozeni stavu, kde se prave ve XML nachazime
        if (name == "slozky") and (not self.__inKoktejly):
            self.__inSlozky = False
        elif (name == "koktejly"):
            self.__inKoktejly = False
        elif (name == "nazev"):
            self.__inNazev = False
        elif (name == "cena"):
            self.__inCena = False
        elif (name == "slozka"):
            self.__inSlozka = False
            if self.__inSlozky:
                self.__slozky.append(self.__slozka)
            else:
                # pridani vydaje k aktualnimu koktejlu
                self.__koktejl.addVydaj(self.__slozky, self.__id, self.__mnozstvi)
        elif (name == "koktejl"):
            self.__koktejl.spocitejZisk()  # vypocet zisku z koktejlu
            self.__koktejly.append(self.__koktejl)  # pridani koktejlu do seznamu

    # prekryti metody characters(self, chrs)    
    def characters(self, chrs):
        if self.__inCena:
            if self.__inSlozky:
                self.__slozka.setCena(float(chrs))
            else:
                self.__koktejl.setCena(float(chrs))

        elif self.__inNazev:
            if self.__inSlozky:
                self.__slozka.setNazev(chrs)
            else:
                self.__koktejl.setNazev(chrs)

        elif self.__inSlozka and self.__inKoktejly:
            self.__mnozstvi = float(chrs)


# Procedura, pro tisk koktejlu
def tiskniKoktejly(koktejly):
    print("{0:2s} {1:25s} {2:5s}\t{3:5s}\t{4:5s}".format("id", "nazev", "cena", "vydaj", "zisk"))
    for koktejl in koktejly:
        print("{0:2d} {1:25s} {2:5.2f}\t{3:5.2f}\t{4:5.2f}".format(koktejl.getId(),
                                                                   koktejl.getNazev(),
                                                                   koktejl.getCena(),
                                                                   koktejl.getVydaje(),
                                                                   koktejl.getZisk()))


# Hlavni funkce
def main():
    handler = BarHandler()  # vytvoreni instance handleru
    parser = make_parser()  # vytvoreni instance parseru
    parser.setContentHandler(handler)  # nastaveni handleru

    inFile = open("bar.xml", "r", encoding="UTF-8")  # otevreni souboru pro cteni
    parser.parse(inFile)  # parsovani souboru
    inFile.close()  # zavreni souboru

    koktejly = handler.getKoktejlyList()  # ziskani seznamu koktejlu

    koktejly.sort(key=attrgetter("zisk"), reverse=True)  # serad seznam koktejlu sestupne podle zisku    
    tiskniKoktejly(koktejly)  # serazeny seznam koktejlu vytiskni


main()
