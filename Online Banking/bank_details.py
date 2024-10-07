from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Vaiu1@#",
        database="bank"
    )

def execute_query(query, params=None, fetchone=False, fetchall=False):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = None
    if fetchone:
        result = cursor.fetchone()
    elif fetchall:
        result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        name = request.form.get("uname")
        email = request.form.get("uemail")
        password = request.form.get("upassword")
        query = "INSERT INTO sign_up(name, email, password) VALUES (%s, %s, %s)"
        execute_query(query, (name, email, password))
        return render_template("sign_com.html")
    return render_template("signup.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        query = "SELECT * FROM sign_up WHERE email=%s AND password=%s"
        result = execute_query(query, (email, password), fetchone=True)
        if result:
            return redirect("/user_main")
        return render_template("logfail.html")
    return render_template("login.html")

@app.route("/user_main")
def user_main():
    email = request.form.get("email")
    return render_template("user_main.html", email=email)

@app.route("/create", methods=["POST", "GET"])
def create_account():
    if request.method == "POST":
        email = request.form.get("email")
        acc_no = request.form.get("accno")
        pin = request.form.get("pin")
        query = "UPDATE sign_up SET acc_no=%s, pin=%s WHERE email=%s"
        execute_query(query, (acc_no, pin, email))
        return render_template("cre_end.html")
    return render_template("create.html")

@app.route("/balance_enquiry", methods=["POST", "GET"])
def balance_enquiry():
    if request.method == "POST":
        acc_no = request.form.get("accno")
        pin = request.form.get("pin")
        query = "SELECT balance FROM sign_up WHERE acc_no=%s AND pin=%s"
        result = execute_query(query, (acc_no, pin), fetchone=True)
        if result:
            return render_template("balanceshow.html", acc=acc_no, result=result)
    return "Invalid account or pin"

@app.route("/deposit", methods=["POST", "GET"])
def deposit():
    if request.method == "POST":
        acc_no = request.form.get("accno")
        pin = request.form.get("pin")
        amount = request.form.get("amt")
        update_query = "UPDATE sign_up SET balance = balance + %s WHERE acc_no=%s AND pin=%s"
        execute_query(update_query, (amount, acc_no, pin))
        return render_template("depshow.html", amt=amount)
    return render_template("deposit.html")

@app.route("/withdraw", methods=["POST", "GET"])
def withdraw():
    if request.method == "POST":
        acc_no = request.form.get("accno")
        pin = request.form.get("pin")
        amount = request.form.get("amount")
        check_balance_query = "SELECT balance FROM sign_up WHERE balance > %s AND acc_no=%s AND pin=%s"
        result = execute_query(check_balance_query, (amount, acc_no, pin), fetchone=True)
        if result:
            update_query = "UPDATE sign_up SET balance = balance - %s WHERE acc_no=%s AND pin=%s"
            execute_query(update_query, (amount, acc_no, pin))
            return render_template("withshow.html", wamt=amount)
        return render_template("withelse.html")
    return render_template("withdrawel.html")

@app.route("/mini_statement", methods=["POST", "GET"])
def mini_statement():
    if request.method == "POST":
        acc_no = request.form.get("acc")
        pin = request.form.get("pin")
        query = "SELECT ant_no, deposit, withdraw FROM statement WHERE ant_no=%s AND pin=%s"
        result = execute_query(query, (acc_no, pin), fetchall=True)
        if result:
            return render_template("minishow.html", reslt=result)
    return render_template("mini_statement.html")

@app.route("/logout", methods=["POST", "GET"])
def logout():
    if request.method == "POST":
        email = request.form.get("email")
        return render_template("loutshow.html", mail=email)
    return render_template("logout.html")

@app.route("/signout", methods=["POST", "GET"])
def signout():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        query = "DELETE FROM sign_up WHERE email=%s AND password=%s"
        execute_query(query, (email, password))
        return render_template("soutshow.html", mail=email)
    return render_template("signout.html")

if __name__ == "__main__":
    app.run(debug=True)
