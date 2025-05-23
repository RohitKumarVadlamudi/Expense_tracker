from flask import Flask, render_template, request
import sqlite3 as sq

app = Flask(__name__)


@app.route("/")

def home():
	conn = sq.connect("expenses.db")
	cursor=conn.cursor()

	cursor.execute("""SELECT DISTINCT strftime('%m', date), strftime('%Y', date) FROM expenses""")
	month_year=cursor.fetchall()
	selected_month=request.args.get("month")
	selected_year=request.args.get("year")
	if selected_month and selected_month:
		cursor.execute("""SELECT*FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?""", (selected_month,selected_year))
	else:
		cursor.execute("""SELECT*FROM expenses""")
	expenses=cursor.fetchall()
	conn.close()
	return render_template("home.html", month=[item[0] for item in month_year], year= [item[1] for item in month_year], expenses=expenses)

if __name__=="__main__":
	app.run(debug=True)