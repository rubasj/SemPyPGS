# potrebne pro DOM
from xml.dom import minidom as dom
from xml.dom import Node

# potrebne pro razeni ...
from operator import attrgetter

# domenova trida - Slozka, vyuziva anotaci
class Slozka:
    def __init__(self, idcko, nazev, cena):
        self.__id    = idcko
        self.__nazev = nazev
        self.__cena  = cena

    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, idcko):
        self.__id = idcko

    @property
    def nazev(self):
        return self.__nazev
    
    @nazev.setter            
    def nazev(self, nazev):
        self.__nazev = nazev

    @property
    def cena(self):
        return self.__cena
    
    @cena.setter   
    def cena(self, cena):
        self.__cena = cena

# domenova trida Koktejl, vyuziva anotaci
class Koktejl:
    def __init__(self, idcko, nazev, cena):
        self.__id     = idcko
        self.__nazev  = nazev
        self.__cena   = cena
        self.__vydaje = 0
        self.__zisk   = 0
    
    @property
    def id(self):
        return self.__id
    
    @id.setter
    def id(self, idcko):
        self.__id = idcko
        
    @property
    def nazev(self):
        return self.__nazev;
    
    @nazev.setter
    def nazev(self, nazev):
        self.__nazev = nazev
        
    @property
    def cena(self):
        return self.__cena
    
    @cena.setter
    def cena(self, cena):
        self.__cena = cena
        
    @property
    def zisk(self):
        return self.__zisk
    
    @property
    def vydaje(self):        
        return self.__vydaje
    
    def spocitejZisk(self):
        self.__zisk = self.__cena - self.__vydaje
            
    def addVydaj(self, slozky, idcko, mnozstvi):
        for slozka in slozky:
            if (slozka.id == idcko):
                self.__vydaje += mnozstvi * slozka.cena
                break
    
# funkce, ktera vraci nacteny seznam slozek    
def nactiSlozky(uzelSlozky):
    
    slozky = []    
    uzly = uzelSlozky.childNodes    
    
    for uzel in uzly:
        if uzel.nodeType == Node.ELEMENT_NODE and uzel.nodeName == "slozka":                                    
            slozka = Slozka(int(uzel.attributes.get("id").value),
                            uzel.getElementsByTagName("nazev")[0].firstChild.data,
                            float(uzel.getElementsByTagName("cena")[0].firstChild.data))
            slozky.append(slozka)
    return slozky

# procedura, ktera aktualnimu koktejlu spocita jeho vydaje        
def slozkyKoktejlu(uzelSlozky, koktejl, slozky):
    
    uzly = uzelSlozky.childNodes
    
    for uzel in uzly:
        if uzel.nodeType == Node.ELEMENT_NODE and uzel.nodeName == "slozka":            
            koktejl.addVydaj(slozky, int(uzel.attributes.get("id").value), float(uzel.firstChild.data))

# funkce, ktera vraci nacteny seznam koktejlu, ktere maji spocitane vydaje a zisk
def nactiKoktejly(uzelKoktejly, slozky):
    
    koktejly = []    
    uzly = uzelKoktejly.childNodes
    
    for uzel in uzly:
        if uzel.nodeType == Node.ELEMENT_NODE and uzel.nodeName == "koktejl":            
            koktejl = Koktejl(int(uzel.attributes.get("id").value),
                              uzel.getElementsByTagName("nazev")[0].firstChild.data,
                              float(uzel.getElementsByTagName("cena")[0].firstChild.data))
            
            slozkyKoktejlu(uzel.getElementsByTagName("slozky")[0], koktejl, slozky)
            
            koktejl.spocitejZisk()
            koktejly.append(koktejl)
    return koktejly

# procedura, pro tisk koktejlu
def tiskniKoktejly(koktejly):
    print ("{0:2s} {1:25s} {2:5s}\t{3:5s}\t{4:5s}".format("id", "nazev", "cena", "vydaj", "zisk"))
    for koktejl in koktejly:
        print ("{0:2d} {1:25s} {2:5.2f}\t{3:5.2f}\t{4:5.2f}".format(koktejl.id, koktejl.nazev, koktejl.cena, koktejl.vydaje, koktejl.zisk))

# zde zacina skript
if __name__ == '__main__':
    
    inFile = open("bar.xml", "r", encoding="UTF-8")      # otevreni souboru pro cteni
    doc = dom.parse(inFile)                              # nacteni celeho XML dokumentu do pameti
    
    korenovyUzel = doc.documentElement                   # ziskani korenoveho elementu
    korenovyUzel.normalize()                             # jeho normalizace
    
    uzly = korenovyUzel.childNodes                       # ziskani primych potomku daneho uzlu
    
    for uzel in uzly:                        
        if uzel.nodeName == "slozky":                    # je-li potomkem uzel "slozky"
            slozky = nactiSlozky(uzel)                   # vytvor seznam slozek
        if uzel.nodeName == "koktejly":                  # je-li potomkem uzel "koktejly"
            koktejly = nactiKoktejly(uzel, slozky)       # vytvor seznam koktejly
          
    inFile.close()                                       # zavri soubor        
    koktejly.sort(key=attrgetter("zisk"), reverse=True)  # serad seznam koktejlu sestupne podle zisku  
    tiskniKoktejly(koktejly)                             # serazeny seznam koktejlu vytiskni
