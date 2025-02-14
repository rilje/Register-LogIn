import mysql.connector
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="", # ako niste nista menjali u phpmyadminu ovo su standardni
    # username i password
	database="backend_projekat" # iz phpmyadmin 
    )


class User:
    __email : str
    __username : str
    __password : str

    def __init__(self,email,username,password):
        self.__email = email
        self.__username = username
        self.__password = password


    def __str__(self):
        rez = f'Email: {self.__email}\nUsername: {self.__username}\nPassword: {self.__password}'
        return rez
    
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password

    @staticmethod
    def registruj(email,username,password,confirm_password):
        greska = ""

        if email == "" or username == "" or password == "" or confirm_password == "":
            greska = "Popunite sva polja."
            return greska

        if "@" not in email or "." not in email:
            greska = "Unesite validnu email adresu"
            return greska
        
        if User.proveri_da_li_email_postoji(email):
            greska = "Email zauzet"
            return greska

        if User.proveri_da_li_username_postoji(username):
            greska = "Username zauzet"
            return greska
        
        if password != confirm_password:
            greska = "Sifre se ne poklapaju"
            return greska
        
        if len(password) < 5:
            greska = "Prekratka sifra"
            return greska

        if not User.validiraj_sifru(password):
            greska = "Sifra mora da sadrzi karaktere i bar jedan broj"
            return greska
        
        sql_upit = "INSERT INTO users (email,username,password) VALUES(%s,%s,%s)"
        parametri = (email,username,password)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()
        return greska
        
        
    
    @staticmethod
    def proveri_da_li_username_postoji(username):
        sql_upit = "SELECT * FROM  users WHERE username = %s"
        parametri = (username,)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql_upit,parametri)
        korisnik = cursor.fetchone()
        if korisnik:
            return True
        return False
    
    @staticmethod
    def validiraj_sifru(password):

        brojac_int = 0
        n = len(password)
        for i in range(n):
            if password[i].isdigit():
                brojac_int += 1
            print(password[i])
        if brojac_int == 0:
            return False
        return True
    
    @staticmethod
    def proveri_da_li_email_postoji(email):
        sql_upit = "SELECT * FROM users WHERE email=%s"
        parametri = (email,)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql_upit,parametri)
        korisnik = cursor.fetchone()
        if korisnik: 
            return True
        return False
         
    @staticmethod
    def loguj(username,password):
        greska = ""
        if username == "" or password == "":
            greska = "Popunite sva polja"
            return greska
        

        if not User.dohvati_korisnika_po_username(username):
            greska = "Username nije pronadjen"
            return greska
        korisnik = User.dohvati_korisnika_po_username(username)
        if korisnik['password'] != password:
            greska = "Netacna sifra"
            return greska

        return greska
        
    @staticmethod
    def dohvati_korisnika_po_username(username):
        sql_upit = "SELECT * FROM users WHERE username = %s"
        parametri = (username,)
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql_upit,parametri)
        if cursor.rowcount == 0:
            return False
        korisnik = cursor.fetchone()
        print(korisnik)
        return korisnik
    

    @staticmethod
    def dohvati_korisnike():
        sql_upit = "SELECT * FROM users"
        cursor = mydb.cursor(dictionary=True)
        cursor.execute(sql_upit)
        if cursor.rowcount == 0:
            return False
        korisnici = cursor.fetchall()
        print(korisnici)
        return korisnici

    @staticmethod
    def obrisi_korisnika(id):
        sql_upit = "DELETE FROM users WHERE id=%s"
        parametri = (id,)
        cursor = mydb.cursor(prepared=True)
        cursor.execute(sql_upit,parametri)
        mydb.commit()
