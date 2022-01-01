import sqlite3

conn = sqlite3.connect("accounts.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS accounts (id int, username VARCHAR(255));""")

# c.execute("INSERT INTO accounts values(1, 'Sidney');")

for i in c.execute("SELECT * FROM accounts;"):
    print(i)
conn.close()
