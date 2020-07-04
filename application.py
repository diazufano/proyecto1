import os
import requests

from flask import Flask, session
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
conexion="postgresql://postgres:11887010@localhost/edx50"

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(conexion)
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    res = requests.get (" https://www.goodreads.com/book/review_counts.json", params =
    {" key ":"dZGnlkLsiELtLnSrHQThzA", "isbns": "0743269268"})
    print (res.text)

if __name__ == "__index__":
    index()

app.run()
