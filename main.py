from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = "secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'redetpion66'
app.config['MYSQL_DB'] = 'python'

mysql = MySQL(app)
@app.route('/auth', methods=['GET','POST'])

def login():
    msg=''
    if request.method == 'POST' and 'id' in request.form:
        id = request.form['id']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * from estudiantes WHERE id =%s ', (id,))
        account = cursor.fetchone()

        if account:
            session['loggedin'] = True 
            session['ind'] = account['ind']
            session['id'] = account['id']

            return redirect(url_for('home'))
        else:
            msg = 'ID incorrecto!'

    
    return render_template("index.html", msg='')

@app.route('/auth/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('ind', None)
    session.pop('id', None)

    return redirect(url_for('login'))

@app.route('/auth/home')
def home():
    if 'loggedin' in session:
        return render_template("home.html", id=session['id'])
    return redirect(url_for('login'))
