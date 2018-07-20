import csv
import sqlite3 as sql


def reader():
	with sql.connect("database.db") as con:
		cur = con.cursor()
		reader = csv.reader(open('j.csv','r'),delimiter=';')
		for row in reader:
			to_db = [unicode(row[0], "utf8"),unicode(row[1], "utf8"),unicode(row[2], "utf8")]
			cur.execute("INSERT INTO books (name,author,category) VALUES (?,?,?);",to_db)
		con.commit()

reader()
