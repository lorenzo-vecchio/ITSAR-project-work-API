from flask import Flask, request, jsonify, make_response, session, Response
from flask_cors import CORS, cross_origin
import pymysql.cursors
from data import DatabaseConnector

app = Flask(__name__)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = "None"
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, supports_credentials=True, resources={r"/*": {"origins": ["http://localhost:3000", "https://itsar-project-work-react.vercel.app"]}}, allow_headers="*")

app.secret_key = 'fdfd'

db_connection_info = {
    "user": "root",
    "password": "mAm7acshQgItFwF4Ze54",
    "host": "containers-us-west-167.railway.app",
    "port": 7433,
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
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
            mail = request.json['mail']
        except KeyError:
            return make_response('ERROR: username, password, or mail missing', 400)
        user = data.execute_query("SELECT id, userName FROM utenti WHERE userName = %s AND password = %s", (username, password))
        if not user:
            data.execute_insert("INSERT INTO utenti (userName, password, email) VALUES (%s, %s, %s);", (username, password, mail))
            user_id = data.execute_query("SELECT id FROM utenti WHERE userName = %s AND password = %s", (username, password))
            session['user_id'] = user_id[0][0]
        else:
            session['user_id'] = user[0][0]
        session['username'] = username
        return make_response('logged in', 200)

        

@app.route("/login", methods=['GET', 'POST'])
def login():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
        except KeyError:
            return make_response('ERROR: username or password missing', 400)
        user = data.execute_query("SELECT id, userName FROM utenti WHERE userName = %s AND password = %s", (username, password))
        if not user:
            return make_response('not valid username or password', 401)
        session['user_id'] = user[0][0]
        session['username'] = username
        return make_response('logged in', 200)
    if request.method == 'GET':
        if 'username' in session and 'user_id' in session:
            return make_response('logged in', 200)
        else:
            return make_response('not logged', 401)

        
        
@app.route("/animals", methods=['GET', 'POST'])
def animals():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if 'username' in session and 'user_id' in session:
        if request.method == 'GET':
            query = """
            SELECT animali.nomeAnimale, animali.sesso, animali.data_di_nascita, razze.nomeRazza, specie.nomeSpecie
            FROM animali
            INNER JOIN razze ON animali.id_razza = razze.id
            INNER JOIN specie ON razze.id_specie = specie.id
            WHERE animali.id_utente = %s;
            """
            rows = data.execute_query(query, (session.get('user_id'),))
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
        if request.method == 'POST':
            try:
                nome_animale = request.json['nome_animale']
                sesso = request.json['sesso']
                data_di_nascita = request.json['data_di_nascita']
                razza = request.json['razza'].lower()
            except KeyError:
                return make_response('ERROR: Missing data for animal creation', 400)
            result = data.execute_query("SELECT id FROM razze WHERE nomeRazza = %s", (razza,))
            if result:
                id_razza = result[0][0]
            else:
                return make_response('ERROR: Razza not found', 400)
            query = """
            INSERT INTO animali (nomeAnimale, sesso, data_di_nascita, id_razza, id_utente)
            VALUES (%s, %s, %s, %s, %s);
            """
            data.execute_insert(query, (nome_animale, sesso, data_di_nascita, id_razza, session.get('user_id')))
            return make_response('Animal created', 200)
    return make_response('Not logged', 401)

@app.route("/servizi", methods=['GET'])
def servizi():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if 'username' in session and 'user_id' in session:
        if request.method == 'GET':
            query = """
            SELECT s.nomeLuogo, s.latitudine, s.longitudine, ts.nomeTipo, l.nomeLocalita, l.provincia, l.regione
            FROM servizi AS s
            JOIN tipologia_servizi AS ts ON s.id_tipo_servizio = ts.id
            JOIN localita AS l ON s.id_localita = l.id;
            """
            rows = data.execute_query(query)
            if rows is None:
                return make_response('Error retrieving data from the database', 500)
            servizi = []
            for row in rows:
                servizio = {
                    'nomeLuogo': row[0],
                    'latitudine': row[1],
                    'longitudine': row[2],
                    'nomeTipo': row[3],
                    'nomeLocalita': row[4],
                    'provincia': row[5],
                    'regione': row[6]
                }
                servizi.append(servizio)
            return jsonify(servizi)
    return make_response('not logged', 401)


@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return make_response('logged out', 200)
    
if __name__ == '__main__':
    app.run(debug=False)