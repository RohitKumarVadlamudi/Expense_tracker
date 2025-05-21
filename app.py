from flask import Flask, render_template
import sqlite3 as sq

app = Flask(__name__)


@app.route("/")

def home():
	conn = sq.connect("expenses.db")
	cursor=conn.cursor()
	cursor.execute("""SELECT*FROM expenses""")
	expenses=cursor.fetchall()
	conn.close()
	return render_template("home.html", expenses=expenses)

if __name__=="__main__":
	app.run(debug=True)