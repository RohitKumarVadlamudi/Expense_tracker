from flask import Flask, render_template, request, flash, redirect
import sqlite3 as sq

app = Flask(__name__)
app.secret_key="0541tran98"

# Home page 

@app.route("/")

def home():
	return render_template("home.html")

# Transactions page

@app.route("/transactions")
def transactions():
    conn = sq.connect("expenses.db")
    cursor = conn.cursor()

    # Get unique month/year from expenses
    cursor.execute("""SELECT DISTINCT strftime('%m', date), strftime('%Y', date) FROM expenses""")
    month_year = cursor.fetchall()

    # Get categories for dropdown in popup
    cursor.execute("""SELECT name FROM category""")
    category_list = [row[0] for row in cursor.fetchall()]

    selected_month = request.args.get("month")
    selected_year = request.args.get("year")

    if selected_month and selected_year:
        cursor.execute("""SELECT * FROM expenses WHERE strftime('%m', date) = ? AND strftime('%Y', date) = ?""", (selected_month, selected_year))
    else:
        cursor.execute("""SELECT * FROM expenses""")

    expenses = cursor.fetchall()
    conn.close()
    return render_template("transactions.html",
                           month=[item[0] for item in month_year],
                           year=[item[1] for item in month_year],
                           expenses=expenses,
                           category=category_list)


# add a transaction

@app.route("/add", methods=["POST"])
def add():
    conn = sq.connect("expenses.db")
    cursor = conn.cursor()
    date = request.form['date']
    amount = request.form['amount']
    category = request.form['category']
    notes = request.form['notes']
    cursor.execute(
        """INSERT INTO expenses (date, amount, category, notes) VALUES (?, ?, ?, ?)""",
        (date, amount, category, notes)
    )
    conn.commit()
    conn.close()
    flash("Transaction added")
    return redirect("/transactions")

# add new category to category table

@app.route("/category-add", methods=["POST"])

def category_add(): 	
	conn=sq.connect("expenses.db")
	cursor=conn.cursor()
	category=request.form['category']
	cursor.execute("""INSERT INTO category (name) VALUES (?)""",(category,))
	conn.commit()
	conn.close()
	return render_template("/transactions.html")


# delete a transaction, button in transaction page

@app.route("/delete/<int:id>", methods=["GET", "POST"])

def delete(id):
	conn=sq.connect("expenses.db")
	cursor=conn.cursor()
	cursor.execute("""DELETE FROM expenses WHERE id IS ?""",(id,))
	conn.commit()
	conn.close()
	flash("Transaction deleted successfully")
	return redirect("/transactions")

# edit a transaction, button in transaction page 

@app.route("/edit/<int:id>", methods=["GET", "POST"])

def edit(id):
	conn=sq.connect("expenses.db")
	cursor=conn.cursor()
	if request.method=="POST":
		date=request.form['date']
		amount=request.form['amount']
		category=request.form['category']
		notes=request.form['notes']
		cursor.execute("""UPDATE expenses SET amount=?, category=?, notes=? WHERE id IS ?""",(amount,category,notes,id))
		conn.commit()
		conn.close()
		flash("Transaction edited successfully")
		return redirect("/transactions")
	else:
		cursor.execute("""SELECT date, amount, category, notes FROM expenses WHERE id IS ?""",(id,))
		row = cursor.fetchone()
		conn.close()
		if row:
			date, amount, category, notes = row
			return render_template("edit.html", id=id, date=date, amount=amount, category=category, notes=notes)
		else:
			flash("Transaction not found")
			return redirect("/transactions")

	return render_template("transactions.html")

# accounts page with a list of all accounts

@app.route("/accounts")

def accounts():
	conn=sq.connect("expenses.db")
	cursor=conn.cursor()
	cursor.execute("""SELECT * FROM accounts""")
	accounts=cursor.fetchall()
	conn.commit()
	conn.close()
	return render_template("accounts.html", accounts=accounts)


# Add a new account to list of accounts

@app.route("/add-acc", methods=["GET", "POST"])

def add_acc():
	if request.method=="POST":
		conn=sq.connect("expenses.db")
		cursor=conn.cursor()
		account=request.form["account"]
		type=request.form['type']
		cursor.execute("""INSERT INTO accounts (account, type) VALUES (?,?)""",(account,type))
		conn.commit()
		conn.close()
		flash("Account Added successfully")
		return redirect("/accounts")
	return render_template("/accounts")

if __name__=="__main__":
	app.run(debug=True)