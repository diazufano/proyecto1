import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgres://dqjmeafvjcfgzi:0f13121def0e4adb5c9a2ccd2db8d86704ea301a74458270a7aa2e5742c0f2b2@ec2-54-247-89-181.eu-west-1.compute.amazonaws.com:5432/d4hr1nh11gu72o')
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
   