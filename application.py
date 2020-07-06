import os
import requests

from flask import Flask, render_template, request, session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_session import Session
from flask import  jsonify     

app = Flask(__name__)
app.secret_key = '11887010'

app.run

engine = create_engine('postgres://dqjmeafvjcfgzi:0f13121def0e4adb5c9a2ccd2db8d86704ea301a74458270a7aa2e5742c0f2b2@ec2-54-247-89-181.eu-west-1.compute.amazonaws.com:5432/d4hr1nh11gu72o')
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
            user = db.execute("SELECT id, name, password FROM users WHERE  password= :inpass",
                    {"inpass": usrpass}).fetchone()
            if user is None:
                error='The user is not registered'
                return render_template('error.html', message=error) 
            else:
                msg='the user exist in the DataBase.'
                # add user=user
                session["user_id"]=user.id
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
    if request.method == 'POST':
        button_click= request.values.get('logout')
        if button_click == 'logout': 
            session.pop("user_id", None)
            session.pop("book_id",None)
            return render_template('index.html') 
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
    if request.method == 'POST':
        button_click= request.values.get('logout')
        if button_click == 'logout': 
            session.pop("user_id", None)
            session.pop("book_id",None)
            return render_template('index.html') 
        button_click= request.values.get('button')
        if button_click == 'review':
            print('hace el review') 
            return render_template('review.html') 
        else:
            msg = 'Button rating no action.'
            return render_template('error.html', message=msg)              
    book_id = request.values.get("book_id")
    session["book_id"]=book_id
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
    #coments of books there
    # 			    
@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        button_click= request.values.get('logout')
        if button_click == 'logout':
            session.pop("user_id", None)
            session.pop("book_id",None)
            return render_template('index.html') 
        button_click= request.values.get('button')
        if button_click == 'Send':
            opinion = request.values.get('opinion')
            if opinion is "":
                msg = 'No make a opinion.'
                return render_template('error.html', message=msg)
            else:      
                print(opinion)
                book_id=session["book_id"]
                user_id=session["user_id"]
                print(book_id)
                print(user_id)
                db.execute("INSERT INTO coments (coment, book_id, user_id) VALUES (:coment, :book_id, :user_id)",
                    {"coment": opinion, "book_id": book_id, "user_id": user_id})
                db.commit()
                msg = 'Realiza el send.'
                return render_template('exito.html', message=msg) 
        return render_template('review.html')            
    else:
        msg = 'No hace POST review.'
        return render_template('error.html', message=msg) 

# ... other imports, set up code, and routes ...
@app.route("/api/<int:book_isbn>", methods=['GET', 'POST'])
def book_api(book_isbn):

#Return details about a single book."""
# Make sure book exists.
    myisbn=str(book_isbn)
    book = db.execute("SELECT * from goodbooks WHERE isbn=:book_isbn",
            {"book_isbn": "0142501085"}).fetchone()
    if book is None:
        return jsonify({"error": "Invalid book_isbn"}), 422
    else:
        return jsonify({
            "title": book.title,
            "author": book.author,
            "year": book.anyo,
            "isbn": book.isbn,
            "review_count": 28,
            "average_score": 5.0
        })

app.run()
