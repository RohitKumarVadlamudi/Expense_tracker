import sqlite3 as sq

conn=sq.connect("expenses.db")

cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS expenses(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	date TEXT NOT NULL,
	amount REAL NOT NULL,
	category TEXT NOT NULL,
	notes TEXT)""");

cursor.execute("""CREATE TABLE IF NOT EXISTS accounts(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	account TEXT NOT NULL,
	type TEXT NOT NULL)""");

conn.commit()
conn.close()