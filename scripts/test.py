import sqlite3

connection = sqlite3.connect('../instance/db.sqlite')

cur = connection.cursor()

data = cur.execute('SELECT * FROM blocks where student="s92"').fetchall()
print(data)

connection.close()