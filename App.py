from math import ceil
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import os,time

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para las sesiones

# Base de datos de usuarios registrados (para fines de demostración solamente)
users = {
    'admin': {'username': 'admin', 'password': 'admin', 'name': 'admin', 'telefono': '123456789'},
    'usuario1': {'username': 'usuario1','password': 'contrasena1', 'name': 'usuario1', 'telefono': '123456789'},
    'usuario2': {'username': 'usuario2','password': 'contrasena2', 'name': 'usuario2', 'telefono': '123456789'},
    'usuario3': {'username': 'usuario3','password': 'contrasena3', 'name': 'usuario3', 'telefono': '123456789'}
}

bikes = {
    '1': {"id": 1, "model": "Mountain Bike", "available": True},
    '2': {"id": 2, "model": "City Bike", "available": True},
    '3': {"id": 3, "model": "BMX Bike", "available": False},
    '4': {"id": 4, "model": "Road Bike", "available": True},
    '5': {"id": 5, "model": "Tandem Bike", "available": True},
    '6': {"id": 6, "model": "Electric Bike", "available": True},
    '7': {"id": 7, "model": "Folding Bike", "available": True},
    '8': {"id": 8, "model": "Cruiser Bike", "available": True},
    '9': {"id": 9, "model": "Kids Bike", "available": True},
    '10': {"id": 10, "model": "Recumbent Bike", "available": True},
    '11': {"id": 11, "model": "Fat Bike", "available": True},
    '12': {"id": 12, "model": "Triathlon Bike", "available": True},
    '13': {"id": 13, "model": "Track Bike", "available": True},
    '14': {"id": 14, "model": "Touring Bike", "available": True},
    '15': {"id": 15, "model": "Cyclocross Bike", "available": True},
}

rentals = {
    'usuario1': {"id": 3, "model": "BMX Bike", "startdate": "2020-10-10 10:00", "status": "rented"},
}

rentals_history = {
    'usuario1': [{"id": 1, "model":"Mountain Bike", "startdate": "2020-10-10 10:00", "enddate":"2020-10-11 10:00" , "price":200, "status": "returned"}],
}

# Esta ruta es para la página principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', bikes=bikes, username=username, rentals=rentals)
    else:
        return render_template('index.html', bikes=bikes)

# Esta ruta es para iniciar sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]["password"] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    else:
        return render_template('login.html')

# Esta ruta es para cerrar la sesión del usuario
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

# Esta ruta es para registrar un nuevo usuario
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        telefono = request.form['telefono']
        if username in users:
            return render_template('register.html', error='Ese nombre de usuario ya está en uso')
        else:
            users[username] = {'username': username, 'password': password, 'name': name, 'telefono': telefono}
            session['username'] = username
            return redirect(url_for('index'))
    else:
        return render_template('register.html')

# Esta ruta es para mostrar la lista de usuarios registrados
@app.route('/users')
def user_list():
    if len(users.keys()) > 0:
        return render_template('user_list.html', users=users)
    else:
        return render_template('404.html'), 404

# Esta ruta es para mostrar la información de un usuario en específico
@app.route('/users/<username>', methods=['GET','POST'])
def user(username):
    if request.method == 'POST':
        if request.form['action'] == 'delete':
            users.pop(username, None)
            return redirect(url_for('user_list'))
        else:
            return render_template('404.html'), 404
    if username in users:
        return render_template('user.html', user=users[username], rentals=rentals, rentals_history=rentals_history,session=session)
    else:
        return render_template('404.html'), 404

# Esta ruta es para mostrar la información de una bicicleta en específico
@app.route('/bike/<bike_id>')
def bike(bike_id):
    if bike_id in bikes:
        return render_template('bike.html', bike=bikes[bike_id], session=session, rentals=rentals)
    else:
        return render_template('404.html'), 404

# Esta ruta es para rentar o devolver una bicicleta
@app.route('/bike/<bike_id>/<action>', methods=['GET','POST'])
def rent_bike(bike_id,action):
    if request.method == 'POST':
        if action == 'rent':
            if bike_id in bikes and bikes[bike_id]["available"]:
                bikes[bike_id]["available"] = False
                rentals[session['username']] = bikes[bike_id]
                rentals[session['username']]['startdate'] = time.strftime("%Y-%m-%d %H:%M")
                rentals[session['username']]['status'] = "rented"
                return redirect(url_for('index'))
            else:
                return render_template('404.html'), 404
        elif action == 'return':
            if bike_id in bikes and not bikes[bike_id]["available"]:
                bikes[bike_id]["available"] = True
                rentals[session['username']]['enddate'] = time.strftime("%Y-%m-%d %H:%M")
                rentals[session['username']]['price'] = calculaprecio(rentals[session['username']]['startdate'],rentals[session['username']]['enddate'])
                rentals[session['username']]['status'] = "returned"
                if session['username'] in rentals_history:
                    rentals_history[session['username']].append(rentals[session['username']])
                else:
                    rentals_history[session['username']] = []
                    rentals_history[session['username']].append(rentals[session['username']])
                rentals.pop(session['username'], None)
                return redirect(url_for('index'))
            else:
                return render_template('404.html'), 404
        else:
            return render_template('404.html'), 404
    else:
        return render_template('404.html'), 404
    
# Esta ruta es para mostrar las bicicletas en renta actualmente
@app.route('/rentals')
def rental():
    return render_template('rentals.html', rentals=rentals)

def calculaprecio(startdate,enddate):
    start = time.strptime(startdate, "%Y-%m-%d %H:%M")
    end = time.strptime(enddate, "%Y-%m-%d %H:%M")
    lapse = round((time.mktime(end) - time.mktime(start)) / 60,0)
    if (lapse <= 3600):
        price = 30
    else:
        price = 30 + ceil((lapse - 3600)) * 10
    return price

if __name__ == '__main__':
    app.run(debug=True)
