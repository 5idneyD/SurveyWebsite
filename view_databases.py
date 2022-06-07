import sqlite3

conn = sqlite3.connect("./users.sqlite3")
c = conn.cursor()

for i in c.execute("SELECT * FROM users;"):
    print("User", i[0],": ", i[1])

conn.close()