import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Person, Base


engine = create_engine('sqlite:///people_rest_db.sqlite')
Session = sessionmaker()
Session.configure(bind=engine)
Base.metadata.create_all(engine)


#conn = sqlite3.connect('people_rest_db.sqlite')
s = Session()

people = [
    Person(id=1,name='Vasya',salary=15000.00,birthday='01-01-1989'),
    Person(id=2,name='Kolya',salary=30000.00,birthday='01-01-1960'),
    Person(id=3,name='Fedya',salary=40000.00,birthday='01-01-1989'),
    Person(id=4,name='Max',salary=20000.00,birthday='01-01-1990'),
    Person(id=5,name='Masha',salary=17000.00,birthday='01-01-19876'),
]

s.bulk_save_objects(people)
s.commit()
s.close()
