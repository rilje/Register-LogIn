import mysql.connector
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", # ako niste nista menjali u phpmyadminu ovo su standardni
    # username i password
	database="backend_projekat" # iz phpmyadmin 
    )

class Post:
    __naslov : str
    __sadrzaj : str
    __id_korisnika : int

    def __init__(self,naslov,sadrzaj,id_korisnika):
        self.__naslov = naslov
        self.__sadrzaj = sadrzaj
        self.__id_korisnika = id_korisnika
    def __str__(self):
        rez = f"Naslov: {self.__naslov}\nSadrzaj: {self.__sadrzaj}\nID korisnika: {self.__id_korisnika}\n"
        return rez
    
    def get_naslov(self):
        return self.__naslov
    def get_sadrzaj(self):
        return self.__sadrzaj
    def get_id_korisnika(self):
        return self.__id_korisnika
    
    @staticmethod
    def dohvati_korisnika_po_id(id):
        sql_upit = "SELECT * FROM users WHERE id=%s"
        parametri = (id,)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql_upit,parametri)
        korisnik = cursor.fetchone()
        if korisnik: 
            return True
        return False
    
    @staticmethod
    def dodaj_objavu(naslov,sadrzaj,id_korisnika):
        greska = ""
        if naslov == "" or sadrzaj == "" or id_korisnika == "":
            greska = "Popunite sva polja."
            return greska
        if len(naslov) < 10:
            greska = "Prekratak naslov"
            return greska
        if len(naslov) > 50:
            greska = "Predugacak naslov"
            return greska
        if  not isinstance(id_korisnika,int):
            greska = "ID korisnika mora biti cifra!"
            return greska
        # MORAM DA PROVERIM DA LI POSTOJI USER SA TIM id-jem
        if not Post.dohvati_korisnika_po_id(id_korisnika):
            greska = "Korisnik sa unetim ID-jem ne postoji u bazi!"
            return greska

        sql_upit = "INSERT INTO post (naslov,sadrzaj,id_korisnika) VALUES (%s,%s,%s)"
        parametri = (naslov,sadrzaj,id_korisnika)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()

        return greska
    
    @staticmethod
    def obrisi_objavu(broj_objave):
        sql_upit = "DELETE FROM post WHERE broj_objave=%s"
        parametri = (broj_objave,)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()


    @staticmethod
    def prikazi_objave():
        sql_upit = "SELECT * FROM post"
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql_upit)
        if cursor.rowcount == 0:
            return False
        objave = cursor.fetchall()
        return objave
    
    @staticmethod
    def update(broj_objave,naslov,sadrzaj,id_korisnika):
        greska = ""
        if naslov == "" or sadrzaj == "" or id_korisnika == "":
            greska = "Popunite sva polja."
            return greska
        if len(naslov) < 10:
            greska = "Prekratak naslov"
            return greska
        if len(naslov) > 50:
            greska = "Predugacak naslov"
            return greska
        if  not isinstance(id_korisnika,int):
            greska = "ID korisnika mora biti cifra!"
            return greska
        # MORAM DA PROVERIM DA LI POSTOJI USER SA TIM id-jem
        if not Post.dohvati_korisnika_po_id(id_korisnika):
            greska = "Korisnik sa unetim ID-jem ne postoji u bazi!"
            return greska
        
        # Ako je  validacija uspesno prosla, radim sql_upit
        sql_upit = "UPDATE post SET naslov=%s,sadrzaj=%s,id_korisnika=%s WHERE broj_objave=%s" 
        parametri = (naslov,sadrzaj,id_korisnika,broj_objave)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()
        return greska
    
    @staticmethod
    def dohvati_objave_korisnika(id_korisnika):
        sql_upit = "SELECT * FROM post WHERE id_korisnika=%s"
        parametri = (id_korisnika,)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql_upit,parametri)
        if cursor.rowcount == 0:
            return False
        objave = cursor.fetchall()
        return objave

 
    

    