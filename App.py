from flask import Flask, jsonify, render_template, request, redirect, url_for, session
import os
import time

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para las sesiones

# Base de datos de usuarios registrados (para fines de demostración solamente)
users = {
    'admin': {'password': 'admin', 'name': 'admin', 'telefono': '123456789'},
    'usuario1': {'password': 'contrasena1', 'name': 'usuario1', 'telefono': '123456789'},
    'usuario2': {'password': 'contrasena2', 'name': 'usuario2', 'telefono': '123456789'},
    'usuario3': {'password': 'contrasena3', 'name': 'usuario3', 'telefono': '123456789'}
}

bikes = {
    '1': {"id": 1, "model": "Mountain Bike", "available": True},
    '2': {"id": 2, "model": "City Bike", "available": True},
    '3': {"id": 3, "model": "BMX Bike", "available": False}
}

rentals = {
    'usuario1': {"id": 1, "model":"Mountain Bike", "date": "2020-10-10", "time": "165"}
}

rentals_history = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', bikes=bikes, username=username)
    else:
        return render_template('index.html', bikes=bikes)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users:
            return render_template('register.html', error='Ese nombre de usuario ya está en uso')
        else:
            users[username] = password
            session['username'] = username
            return redirect(url_for('index'))
    else:
        return render_template('register.html')
    
@app.route('/users')
def user_list():
    if len(users.keys()) > 0:
        return render_template('user_list.html', users=users)
    else:
        return render_template('404.html'), 404
    
@app.route('/users/<username>')
def user(username):
    if username in users:
        return render_template('user.html', username=username, rentals_history=rentals_history)
    else:
        return render_template('404.html'), 404

@app.route('/bike/<int:bike_id>')
def bike(bike_id):
    bike = next((bike for bike in bikes if bike["id"] == bike_id), None)
    if bike:
        return render_template('bike.html', bike=bike)
    else:
        return render_template('404.html'), 404

@app.route('/bike/<int:bike_id>/<action>', methods=['POST'])
def rent_bike(bike_id):
    bike = next((bike for bike in bikes if bike["id"] == bike_id), None)
    if bike and bike["available"]:
        bike["available"] = False
        rentals.append(bike)
        return redirect(url_for('index'))
    elif bike:
        return render_template('not_available.html', bike=bike)
    else:
        return render_template('404.html'), 404

@app.route('/rentals')
def rental():
    return render_template('rentals.html', rentals=rentals)

if __name__ == '__main__':
    app.run(debug=True)
