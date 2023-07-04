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

        
        
@app.route("/animals", methods=['GET', 'POST', 'DELETE'])
def animals():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if 'username' in session and 'user_id' in session:
        if request.method == 'GET':
            query = """
            SELECT animali.id, animali.nomeAnimale, animali.sesso, animali.data_di_nascita, animali.peso, razze.nomeRazza, specie.nomeSpecie
            FROM animali 
            INNER JOIN razze ON animali.id_razza = razze.id
            INNER JOIN specie ON razze.id_specie = specie.id
            WHERE animali.id_utente = %s;
            """
            rows = data.execute_query(query, (session.get('user_id'),))
            animals = []
            for row in rows:
                animal = {
                    'id': row[0],
                    'nome_animale': row[1],
                    'sesso': row[2],
                    'data_di_nascita': row[3].strftime("%Y-%m-%d"),
                    'peso': row[4],
                    'nome_razza': row[5],
                    'nome_specie': row[6]
                }
                animals.append(animal)
            return jsonify(animals)
        if request.method == 'POST':
            try:
                nome_animale = request.json['nome_animale']
                sesso = request.json['sesso']
                data_di_nascita = request.json['data_di_nascita']
                razza = request.json['razza'].lower()
                peso = request.json['peso']
            except KeyError:
                return make_response('ERROR: Missing data for animal creation', 400)
            result = data.execute_query("SELECT id FROM razze WHERE nomeRazza = %s", (razza,))
            if result:
                id_razza = result[0][0]
            else:
                return make_response('ERROR: Razza not found', 400)
            query = """
            INSERT INTO animali (nomeAnimale, sesso, data_di_nascita, id_razza, id_utente, peso)
            VALUES (%s, %s, %s, %s, %s, %s);
            """
            data.execute_insert(query, (nome_animale, sesso, data_di_nascita, id_razza, session.get('user_id'), str(peso)))
            return make_response('Animal created', 200)
        if request.method == 'DELETE':
            try:
                id_animale = request.json['id']
            except KeyError:
                return make_response('Non hai inserito i parametri corretti', 400)
            query = """
            DELETE a, r
            FROM animali a
            LEFT JOIN riferimento r ON r.id_animale = a.id
            WHERE a.id = %s AND a.id_utente = %s;
            """
            data.execute_insert(query, (id_animale, session.get('user_id'),))
            return make_response('animale eliminato', 200)
    return make_response('Not logged', 401)

@app.route("/servizi", methods=['GET'])
def servizi():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if 'username' in session and 'user_id' in session:
        if request.method == 'GET':
            try:
                place_id = request.json['id']
            except:
                query = """
                SELECT s.nomeLuogo, s.latitudine, s.longitudine, ts.nomeTipo, l.nomeLocalita, l.provincia, l.regione, s.id
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
                        'nome': row[0],
                        'latitudine': row[1],
                        'longitudine': row[2],
                        'tipo': row[3],
                        'localita': row[4],
                        'provincia': row[5],
                        'regione': row[6],
                        'id': row[7]
                    }
                    servizi.append(servizio)
                return jsonify(servizi)
            query = """
            SELECT nomeLuogo, latitudine, longitudine, id_tipo_servizio, id_localita FROM servizi WHERE id = %s
            """
            row = data.execute_query(query, (place_id))[0]
            place = {
                'nome': row[0],
                'lat': row[1],
                'long': row[2],
            }
            return jsonify(place)
    return make_response('not logged', 401)

@app.route("/preferiti", methods=['GET'])
def preferiti():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if 'username' in session and 'user_id' in session:
        query = """
        SELECT s.id, s.nomeLuogo, l.nomeLocalita, l.provincia
        FROM utenti AS u
        INNER JOIN preferiti AS p ON u.id = p.id_utente 
        INNER JOIN servizi AS s ON p.id_servizi = s.id 
        INNER JOIN localita AS l ON s.id_localita = l.id
        WHERE u.id = %s;
        """
        rows = data.execute_query(query, (session.get('user_id'),))
        luoghi_preferiti = []
        for row in rows:
            luogo_preferito = {
                'id': row[0],
                'nome_luogo': row[1],
                'nome_localita': row[2],
                'provincia': row[3]
            }
            luoghi_preferiti.append(luogo_preferito)
        return jsonify(luoghi_preferiti)
    return make_response('not logged', 401)

@app.route("/promemoria", methods=['GET', 'POST'])
def promemoria():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if 'username' in session and 'user_id' in session:
        if request.method == 'GET':
            query = """
            SELECT pm.id, pm.titolo, pm.descrizione, pm.data_e_ora, GROUP_CONCAT(a.nomeAnimale SEPARATOR ', ') AS animali
            FROM promemoria AS pm
            INNER JOIN riferimento AS r ON pm.id = r.id_promemoria
            INNER JOIN animali AS a ON r.id_animale = a.id
            INNER JOIN utenti AS u ON a.id_utente = u.id
            WHERE u.id = %s AND pm.data_e_ora >= CURDATE()
            GROUP BY pm.id, pm.titolo, pm.descrizione, pm.data_e_ora
            ORDER BY pm.data_e_ora;
            """
            rows = data.execute_query(query, (session.get('user_id'),))
            promemorias = []
            for row in rows:
                promemoria = {
                    'id': row[0],
                    'titolo': row[1],
                    'descrizione': row[2],
                    'data_ora': row[3].strftime("%Y-%m-%dT%H:%M"),
                    'animali': row[4]
                }
                promemorias.append(promemoria)
            return jsonify(promemorias)
        if request.method == 'POST':
            try:
                titolo = request.json['titolo']
                descrizione = request.json['descrizione']
                data_ora = request.json['data_ora'].replace('T', ' ')
                animali = request.json['animali']
            except KeyError:
                return make_response('ERROR: Missing data for promemoria creation', 400)
            query = """
            INSERT INTO promemoria (titolo, descrizione, data_e_ora)
            VALUES (%s, %s, %s);
            """
            promemoria_id = data.execute_insert(query, (titolo, descrizione, data_ora))
            for animale in animali:
                query = """
                INSERT INTO riferimento(id_promemoria, id_animale)
                values (%s,%s);
                """
                data.execute_insert(query, (promemoria_id, animale))
            return make_response('promemoria added', 200)
    return make_response('not logged', 401)

@app.route("/user", methods=['POST', 'GET'])
def user():
    data = DatabaseConnector(db_connection_info)
    data.connect()
    if 'username' in session and 'user_id' in session:
        if request.method == 'POST':
            nome = request.json('nome', None)
            cognome = request.json('cognome', None)
            username = request.json('username', None)
            email = request.json('email', None)
            password = request.json('password', None)
            query = """
            UPDATE `utenti`
            SET `userName` = '%s',
                `password` = '%s',
                `nome` = '%s',
                `cognome` = '%s',
                `email` = '%s'
            WHERE `id` = %s;

            """
            data.execute_query(query, (username, password, nome, cognome, email, session.get('user_id'),))
            return make_response('update successful', 200)
        if request.method == 'GET':
            query = """
            SELECT *
            FROM `utenti`
            WHERE `id` = %s;
            """
            row = data.execute_query(query, (session.get('user_id'),))[0]
            result = {
                'username': row[1],
                'password': row[2],
                'nome': row[3],
                'cognome': row[4],
                'email': row[5],
            }
            return jsonify(result)     
    return make_response('not logged', 401)

@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return make_response('logged out', 200)
    
if __name__ == '__main__':
    app.run(debug=False)