from flask import Flask, make_response, request, session, jsonify, Response
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = "None"
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost"]}}, allow_headers="*")

app.secret_key = 'fdfd'

db_connection_info = {
    "user": "root",
    "password": "mAm7acshQgItFwF4Ze54",
    "host": "containers-us-west-167.railway.app",
    "port": "7433",
    "database": "railway"
}


@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

# 400 = bad request (username or password missing)
# 401 = password or username not valid / not authorized

@app.route("/register", methods=['POST'])
def register():
    cnx = mysql.connector.connect(**db_connection_info)
    cursor = cnx.cursor()
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
            mail = request.json['mail']
        except:
            return make_response('ERROR: username, password or mail missing', 400)
        cursor.execute("SELECT id, userName FROM utenti WHERE userName = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user is None:
            cursor.execute("INSERT INTO utenti (userName, password, email) VALUES (%s, %s, %s);", (username, password, mail))
            id = cursor.lastrowid
            cnx.commit()
        if user is not None:
            session['user_id'] = user[0]
        else:
            session['user_id'] = id
        session['username'] = username
        return make_response('logged in', 200)
        

@app.route("/login", methods=['GET', 'POST'])
def login():
    cnx = mysql.connector.connect(**db_connection_info)
    cursor = cnx.cursor()
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
        except:
            return make_response('ERROR: username or password missing', 400)
        cursor.execute("SELECT id, userName FROM utenti WHERE userName = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user is None:
            return make_response('not valid username or password', 401)
        session['user_id'] = user[0]
        session['username'] = username
        return make_response('logged in', 200)
    if request.method == 'GET':
        if 'username' in session and 'user_id' in session:
            return make_response('logged in', 200)
        else:
            return make_response('not logged', 401)
        
        
@app.route("/animals", methods=['GET', 'POST'])
def animals():
    cnx = mysql.connector.connect(**db_connection_info)
    cursor = cnx.cursor()
    if 'username' in session and 'user_id' in session:
        if request.method == 'GET':
            cursor.execute("SELECT animali.nomeAnimale, animali.sesso, animali.data_di_nascita, razze.nomeRazza, specie.nomeSpecie FROM animali  INNER JOIN razze ON animali.id_razza = razze.id INNER JOIN specie ON razze.id_specie = specie.id WHERE animali.id_utente = '%s';", (session.get('user_id'),))
            rows = cursor.fetchall()
            animals = []
            for row in rows:
                animal = {
                    'nomeAnimale': row[0],
                    'sesso': row[1],
                    'data_di_nascita': row[2],
                    'nomeRazza': row[3],
                    'nomeSpecie': row[4]
                }
                animals.append(animal)
            return jsonify(animals)
    if not ('username' in session and 'user_id' in session):
        return make_response('not logged', 401)

@app.route("/luoghi", methods=['GET'])
def luoghi():
    cnx = mysql.connector.connect(**db_connection_info)
    cursor = cnx.cursor()
    if 'username' in session and 'user_id' in session:
        if request.method == 'GET':
            cursor.execute("SELECT l.nomeLuogo, tl.nomeTipo, loc.nomeLocalita, prov.sigla, reg.nomeRegione, l.latitudine, l.longitudine FROM luoghi AS l JOIN tipo_luoghi AS tl ON l.id_tipo_luogo = tl.id JOIN localita AS loc ON l.id_localita = loc.id JOIN province AS prov ON loc.id_provincia = prov.id JOIN regioni AS reg ON prov.id_regione = reg.id;")
            rows = cursor.fetchall()
            luoghi = []
            for row in rows:
                luogo = {
                    'nome': row[0],
                    'tipo': row[1],
                    'comune': row[2],
                    'provincia': row[3],
                    'regione': row[4],
                    'latitudine': row[5],
                    'longitudine': row[6]
                }
                luoghi.append(luogo)
            return jsonify(luoghi)
    if not ('username' in session and 'user_id' in session):
        return make_response('not logged', 401)

@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return make_response('logged out', 200)
    
if __name__ == '__main__':
    app.run(debug=False)