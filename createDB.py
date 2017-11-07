import sqlite3
databasePath='./mping.db'
conn=sqlite3.connect(databasePath)
cu=conn.cursor()
sql='CREATE TABLE HOST_LATENCY (ID INTEGER PRIMARY KEY AUTOINCREMENT,HOST TEXT NOT NULL,LATENCY INT NOT NULL)'
cu.execute(sql)
conn.commit()
conn.close()