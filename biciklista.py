
class Biciklista:
    __id : int
    __broj_prijave : str
    __sifra : str
    __pol : str
    __prva_etapa : int
    __druga_etapa : int

    def __init__(self,id:int,broj_prijave:str,sifra:str,pol:str,prva_etapa:int,druga_etapa:int):
        self.__id = id
        self.__broj_prijave = broj_prijave
        self.__sifra = sifra
        self.__pol = pol
        self.__prva_etapa = prva_etapa
        self.__druga_etapa = druga_etapa

    def get_id(self):
        return self.__id
    def get_broj_prijave(self):
        return self.__broj_prijave
    def get_sifra(self):
        return self.__sifra
    def get_pol(self):
        return self.__pol
    def get_prva_etapa(self):
        return self.__prva_etapa
    def get_druga_etapa(self):
        return self.__druga_etapa

    def set_broj_prijave(self,nova_prijava):
        self.__broj_prijave = nova_prijava
    def set_pol(self,novi_pol):
        self.__pol = novi_pol
    def set_sifra(self,nova_sifra):
        self.__sifra = nova_sifra
    def set_prva_etapa(self,nova_etapa):
        self.__prva_etapa = nova_etapa
    def set_druga_etapa(self, nova_etapa):
        self.__druga_etapa = nova_etapa
    
    def izracunaj_ukupno_vreme(self):
        ukupno_vreme = self.__prva_etapa + self.__druga_etapa
        sati = ukupno_vreme // 3600
        minuti = (ukupno_vreme % 3600) // 60
        sekunde = (ukupno_vreme % 3600) % 60
        return f"{sati}:{minuti}:{sekunde}"

    def __str__(self) -> str:
        rez = f"ID:{self.__id}\n"
        rez += f"Broj prijave:{self.__broj_prijave}\n"
        rez += f"Pol:{self.__pol}\n"
        rez += f"Sifra:{self.__sifra}\n"
        rez += f"Prva etapa:{self.__prva_etapa}\n"
        rez += f"Druga etapa:{self.__druga_etapa}\n"
        rez += f"Ukupno vreme:{self.izracunaj_ukupno_vreme()}\n"
        return rez

biciklista = Biciklista(1,12,'muski','123',20,30)
print(biciklista)
