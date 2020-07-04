import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://postgres:11887010@localhost/edx50')
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, anyo in reader:
        db.execute("INSERT INTO goodbooks (isbn, title, author, anyo) VALUES (:isbn, :title, :author, :anyo)",
                   {"isbn": isbn, "title": title, "author": author, "anyo": anyo})
        print(f"Added book title {title} by {author} from year {anyo}")
    db.commit()

if __name__ == "__main__":
    main()
   