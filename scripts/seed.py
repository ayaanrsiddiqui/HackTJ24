import sqlite3

connection = sqlite3.connect('../instance/db.sqlite')

with open('seed.sql') as f:
    connection.executescript(f.read())
    pass