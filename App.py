from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Clave secreta para las sesiones

# Base de datos de usuarios registrados (para fines de demostración solamente)
users = {
    'usuario1': 'contrasena1',
    'usuario2': 'contrasena2',
    'usuario3': 'contrasena3'
}

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' in session:
        username = session['username']
        return render_template('index.html', username=username)
    else:
        return redirect(url_for('login'))

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

if __name__ == '__main__':
    app.run(debug=True)
