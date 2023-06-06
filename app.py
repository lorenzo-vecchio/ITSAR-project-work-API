from flask import Flask, make_response, request, session, jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = 'bellabellabella12345678910'

cnx = mysql.connector.connect(user='root', password='password', host='localhost', port='3306', database='project_work')
cursor = cnx.cursor()

# 400 = bad request (username or password missing)
# 401 = password or username not valid

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.json['username']
            password = request.json['password']
        except:
            return make_response('ERROR: username or password missing', 400)
        cursor.execute("SELECT id, userName, email FROM utenti WHERE userName = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user is None:
            make_response('not valid username or password', 401)
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
    if request.method == 'GET':
        if 'username' in session and 'user_id' in session:
            cursor.execute("SELECT animali.nomeAnimale, animali.sesso, animali.data_di_nascita, razze.nomeRazza, specie.nomeSpecie FROM animali INNER JOIN razze ON animali.id_razza = razze.id INNER JOIN specie ON razze.id_specie = specie.id WHERE animali.id_utente = %s;", (session.get('user_id'),))
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


@app.route("/logout", methods=['POST'])
def logout():
    session.clear()
    return make_response('logged out', 200)
    
if __name__ == '__main__':
    app.run(debug=True)