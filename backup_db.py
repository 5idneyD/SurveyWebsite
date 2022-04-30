import sqlite3

conn = sqlite3.connect("users.sqlite3")
bck = sqlite3.connect("/home/SLD/SurveyWebsite/_users_.sqlite3")

with bck:
    conn.backup(bck)

bck.commit()
conn.commit()

bck.close()
conn.close()

print("Database backed up")