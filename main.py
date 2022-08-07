from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask import flash
import  os


app = Flask(__name__)

app.secret_key = "secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'redetpion66'
app.config['MYSQL_DB'] = 'mynewdb'

mysql = MySQL(app)
@app.route('/auth', methods=['GET','POST'])


def login():
    msg=''
   
    if request.method == 'POST' and 'cedula' in request.form:
        cedula = request.form['cedula']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute('SELECT * from estudiantes WHERE cedula =%s ', (cedula,))
       
        
        account = cursor.fetchone()
        print(account)

        
        

        if account:
            session['loggedin'] = True 
            session['ind'] = account['ind']
            session['cedula'] = account['cedula']
            session['nombre'] = account['nombre']
            session['ate'] = account['ate']

            if account['ate']:
                flash("Parece que ya ingresaste " + account['nombre'])
                msg = "Parece que ya ingresaste " + account['nombre']
                
                
                return redirect(url_for('unverified'))
                
                
                

            else:
                flash("Ya puedes almorzar " + account['nombre'])
                msg = "Ya puedes almorzar " + account['nombre']
                cursor.execute('UPDATE estudiantes SET ate = True WHERE cedula =%s ', (cedula,))
                mysql.connection.commit()
                
                return redirect(url_for('modal'))


            

            
            
          

            
        else:
            flash("Cedula incorrecta! Acercate a alguno de los organizadores para mas informacion")
            msg = 'Cedula incorrecta! Acercate a alguno de los organizadores para mas informacion'
            
            return redirect(url_for('unverified'))

            

    
    print()
    return render_template("index.html", msg=msg)

@app.route('/auth/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('ind', None)
    session.pop('cedula', None)

    return redirect(url_for('login'))

@app.route('/auth/home')
def home():
    if 'loggedin' in session:
        return render_template("home.html", id=session['id'])
    return redirect(url_for('login'))

@app.route('/auth/modal')
def modal():

   
    return render_template("modalverified.html")


@app.route('/auth/modalno')
def unverified():

   
    return render_template("modalunverified.html")
   
