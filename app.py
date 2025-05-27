from flask import Flask, render_template, request, flash, redirect
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
		conn= sq.connect("expenses.db")
		cursor=conn.cursor()
		date=request.form['date']
		amount=request.form['amount']
		category=request.form['category']
		notes=request.form['notes']
		cursor.execute("""INSERT INTO expenses ( date, amount, category, notes)
			Values(?,?,?,?)""",(date, amount,category, notes))
		conn.commit()
		conn.close()
		flash("Transaction added")
		return redirect("/accounts-expenses")
	return render_template("accounts.html")


@app.route("/delete/<int:id>", methods=["GET", "POST"])

def delete(id):
	conn=sq.connect("expenses.db")
	cursor=conn.cursor()
	cursor.execute("""DELETE FROM expenses WHERE id IS ?""",(id,))
	conn.commit()
	conn.close()
	flash("Transaction deleted successfully")
	return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])

def edit(id):
	if request.method=="POST":
		conn=sq.connect("expenses.db")
		cursor=conn.cursor()
		date=request.form['date']
		amount=request.form['amount']
		category=request.form['category']
		notes=request.form['notes']
		cursor.execute("""UPDATE expenses SET amount=?, category=?, notes=? WHERE id IS ?""",(amount,category,notes,id))
		conn.commit()
		conn.close()
		flash("Transaction edited successfully")
		return redirect("/")
	else:
		cursor.execute("""FROM expenses SELECT amount, category, notes WHERE id IS ?""",(id,))
		row = cursor.fetchone()
		conn.close()
		if row:
			amount, category, notes = row
			return render_template("edit.html", id=id, amount=amount, category=category, notes=notes)
		else:
			flash("Transaction not found")
			return redirect("/")

	return render_template("home.html")

if __name__=="__main__":
	app.run(debug=True)