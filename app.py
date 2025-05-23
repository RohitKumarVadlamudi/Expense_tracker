from flask import Flask, render_template, request, flash
import sqlite3 as sq

app = Flask(__name__)
app.secret_key="0541tran98"


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

@app.route("/accounts-expenses", methods=["GET","POST"])

def add():
	if request.method=="POST":
		conn=sq.connect("expenses.db")
		cursor=conn.cursor()
		date=request.forms['date']
		amount=request.forms['notes']
		category=request.forms['category']
		notes=request.forms['notes']
		cursor.execute("""INSERT INTO expenses ( date, amount, category, notes)
			Values(?,?,?,?)""",(date, amount,category, notes))
		connect.commit()
		conn.close()
		flash("Transaction added")
		return redirect("accounts.html")
	return render_template("accounts.html")
if __name__=="__main__":
	app.run(debug=True)