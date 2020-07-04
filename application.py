import os

from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

app.run

engine = create_engine('postgresql://postgres:11887010@localhost/edx50')
db = scoped_session(sessionmaker(bind=engine))

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def index():
    msg = None
    if request.method == 'POST':
        usrname =request.values.get("username")
        usrpass =request.values.get("password")
        button_click= request.values.get('sub_button')
        if button_click == 'Login':
            user = db.execute("SELECT name, password FROM users WHERE  password= :inpass",
                    {"inpass": usrpass}).fetchone()
            if user is None:
                error='El Usuario no esta registrado'
                return render_template('error.html', message=error) 
            else:
                msg='el usuario esta en la BBDD.'
                return render_template('exito.html', message=msg)            
        if button_click == 'Register':
            user = db.execute("SELECT name, password FROM users WHERE  password= :inpass",
                    {"inpass": usrpass}).fetchone()
            if user is None:
                db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                {"name": usrname, "password": usrpass})
                db.commit()
                msg='se ha registrado correctamente.'
                return render_template('exito.html', message=msg)
            else:
                msg='el usuario esta en la BBDD.'
                return render_template('exito.html', message=msg)  
        return render_template('index.html') 
    return render_template('index.html')    
app.run()
