import os
import requests
#import json


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
                error='The user is not registered'
                return render_template('error.html', message=error) 
            else:
                msg='the user exist in the DataBase.'
                # add user=user
                return render_template('seek.html')            
        if button_click == 'Register':
            user = db.execute("SELECT name, password FROM users WHERE  password= :inpass",
                    {"inpass": usrpass}).fetchone()
            if user is None:
                db.execute("INSERT INTO users (name, password) VALUES (:name, :password)",
                {"name": usrname, "password": usrpass})
                db.commit()
                msg='It has been successfully registered.'
                return render_template('exito.html', message=msg)
            else:
                msg='the user exist in the DataBase.'
                return render_template('exito.html', message=msg)  
        return render_template('index.html') 
    return render_template('index.html') 

@app.route('/seek', methods=['GET', 'POST'])
def seek():
    seek = request.values.get("seek")
    if seek == "":
        msg= 'You must enter a search model.'
        return render_template('error.html', message=msg)
    else: 
        seek='%'
        seek += request.values.get("seek")
        seek+='%'
        lisbn =  db.execute("SELECT * from goodbooks WHERE  isbn like :seek",
                    {"seek": seek}).fetchall()
        ltitle =  db.execute("SELECT * from goodbooks WHERE  title like :seek",
                    {"seek": seek}).fetchall()
        lauthor = db.execute("SELECT * from goodbooks WHERE  author like :seek",
                    {"seek": seek}).fetchall() 
        if (len(lisbn) < 1 and len(ltitle) < 1 and len(lauthor) < 1 ):
            msg='There is no result for that search'
            return render_template('seek.html', message=msg) 
        else:                      
            return render_template('seek.html', lisbn=lisbn, ltitle=ltitle, lauthor=lauthor)  

@app.route('/book', methods=['GET', 'POST'])
def book():
    book_id = request.values.get("book_id")
    book = db.execute("SELECT * from goodbooks WHERE id=:book_id",
                    {"book_id": book_id}).fetchone()
    res = requests.get (" https://www.goodreads.com/book/review_counts.json", params =
    {" key ":"dZGnlkLsiELtLnSrHQThzA", "isbns":book.isbn})
    data = res.json()
    if book is None:
        msg = 'Book not exist in DataBase'
        return render_template('error.html', message=msg) 
    else:                     
        return render_template('book.html', book=book, data=data) 

app.run()
