
from flask import Flask,render_template,request,session,redirect,url_for,json,jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "RAF2021-2022"


from user import User
from post import Post


@app.route('/')
def index():
    return 'Hello world'


@app.route('/registruj',methods=['POST'])
def registruj():
    data = request.get_json()
    email = data['email']
    username = data['username']
    password = data['password']
    confirm_password = data['confirm_password']
    greska = User.registruj(email,username,password,confirm_password)
    if greska != "":
        return jsonify({"data":{"message":f"{greska}"}}), 400
        
    return jsonify({"data":{"message":f"Korisnik '{username}' uspesno registrovan."}}), 200

@app.route('/loguj',methods=['POST'])
def loguj():
    data = request.get_json()
    username = data['username']
    password = data['password']
    greska = User.loguj(username,password)
    if greska != "":
        return  jsonify({"data":{"message":f"{greska}"}}), 400
    session['username'] = username
    print(session['username'])
    return jsonify({"data":{"message":"Korisnik uspesno ulogovan"}}), 200

@app.route('/login_provera')
def login_provera():
    if 'username' not in session:
        return jsonify({"data":{"message":"Korisnik nije ulogovan!"}}), 401
    return jsonify({"data":{"message":"Korisnik ulogovan!"}}), 200

@app.route('/logout')
def logout():
    if 'username' not in session:
        return jsonify({"data":{"message":"Korisnik nije ulogovan, logout nije moguc!"}}), 401
    session.clear()
    return jsonify({"data":{"message":"Korisnik uspesno izlogovan!"}}), 200
      
@app.route('/prikazi_korisnike')
def prikazi_korisnike():
    if not User.dohvati_korisnike():
        return jsonify({"data":{"message":"Nema podataka u bazi"}}), 500
    korisnici = User.dohvati_korisnike()
    return jsonify({"data":{"message":"Uspesno ste dohvatili korisnike iz baze", "korisnici":f"{korisnici}"}}), 200

@app.route('/obrisi_korisnika',methods=['POST'])
def obrisi_korisnika():
    data = request.get_json()
    id = data['id']
    User.obrisi_korisnika(id)
    return jsonify({"data":{"message":f"Uspesno ste obrisali korisnika sa ID-jem: '{id}'"}})

@app.route('/dodaj_objavu',methods=['POST'])
def dodaj_objavu():
    data = request.get_json()
    naslov = data['naslov']
    sadrzaj = data['sadrzaj']
    id_korisnika = data['id_korisnika']
    greska = Post.dodaj_objavu(naslov,sadrzaj,id_korisnika)
    if greska != "":
        return jsonify({"data":{"message":f"{greska}"}}), 401
    return jsonify({"data":{"message":f"Uspesno ste dodali novi post.","objava":f"{data}"}}), 200
    

@app.route('/obrisi_objavu',methods=['POST'])
def obrisi_objavu():
    data = request.get_json()
    broj_objave = data['broj_objave']
    Post.obrisi_objavu(broj_objave)
    return jsonify({"data":{"message":f"Uspesno ste obrisali objavu.",}}), 200

@app.route('/prikazi_objave',methods=['POST'])
def prikazi_objave():
    if not Post.prikazi_objave():
        return jsonify({"data":{"message":f"Nema objava u bazi"}}), 500
    objave = Post.prikazi_objave()
    return jsonify({"data":{"message":f"Uspesno ste dohvatili objave iz baze.","objave":f"{objave}"}}), 200

@app.route('/update',methods=['POST'])
def update():
    data = request.get_json()
    broj_objave = data['broj_objave']
    naslov = data['naslov']
    sadrzaj = data['sadrzaj']
    id_korisnika = data['id_korisnika']
    greska = Post.update(broj_objave,naslov,sadrzaj,id_korisnika)
    if greska != "":
        return  jsonify({"data":{"message":f"{greska}"}}), 400
    return jsonify({"data":{"message":f"Uspesno azurirali objavu sa brojem objave '{broj_objave}'."}}), 200

@app.route('/prikazi_objave_korisnika',methods=['POST'])
def prikazi_objave_korisnika():
    greska = ""
    data = request.get_json()
    id_korisnika = data['id_korisnika']
    if not Post.dohvati_objave_korisnika(id_korisnika):
        greska = "Korisnik nema objave."
        return  jsonify({"data":{"message":f"{greska}"}}), 400
    objave = Post.dohvati_objave_korisnika(id_korisnika)
    return jsonify({"data":{"message":f"Uspesno ste dohvatili objave","objave": f"'{objave}'."}}), 200



app.run(debug=True)