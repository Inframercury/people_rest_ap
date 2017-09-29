import sqlite3
conn = sqlite3.connect('people_rest_db.sqlite')

c = conn.cursor()
# c.execute('CREATE TABLE person (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL )')
#c.execute('INSERT INTO person VALUES (2,"Phil",15000,"01-01-2010")')
#c.execute('UPDATE person SET name="{}" WHERE id={}'.format('Philipp','1'))
c.execute('SELECT sqlite_version()')
conn.commit()
conn.close()