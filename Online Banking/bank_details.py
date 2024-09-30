from flask import Flask,render_template,request,redirect
import mysql.connector

bank=Flask(__name__)

mysql=mysql.connector.connect(
    host="localhost",
    user="root",
    password="Vaiu1@#",
    database="bank"
    )
cursor = mysql.cursor()
# cursor = mysql.cursor(dictionary=True)
@bank.route("/")
def home():
    return render_template("home.html")


@bank.route("/signup",methods=["POST","GET"])
def signup():
    if request.method=="POST":#it is secured
        n=request.form.get("uname")
        e=request.form.get("uemail")
        p=request.form.get("upassword")
        cursor.execute("insert into sign_up(name,email,password) values(%s,%s,%s)",(n,e,p))
        mysql.commit()
        return render_template("sign_com.html")
    return render_template("signup.html")

@bank.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":#it is secured
        em=request.form.get("email")
        pw=request.form.get("password") 
        cursor.execute("select * from sign_up where email=%s and password=%s",(em,pw))
        result=cursor.fetchone()
        mysql.commit()
        if result:
            return redirect("/user_main")
        else:
            return render_template("logfail.html")
    
    return render_template("login.html")

@bank.route("/user_main")
def user_main():
    em=request.form.get("email")
    return render_template("user_main.html",em=em)

@bank.route("/Create",methods=["POST","GET"])
def create_account():
    if request.method == "POST":
        cm = request.form.get("email")
        cacc=request.form.get("accno")
        cpin=request.form.get("pin")
        cursor.execute("update sign_up set acc_no=%s , pin=%s where email=%s",(cacc,cpin,cm))
        mysql.commit()
        return render_template("cre_end.html")
    return render_template("create.html")

@bank.route("/Balance")
def balance():
    return render_template("balance.html")

@bank.route("/balance_enquiry",methods=["POST","GET"])
def balance_enquiry():
    if request.method == "POST":
        bacc=request.form.get("accno")
        bpin=request.form.get("pin")
        cursor.execute("select balance from sign_up where acc_no=%s and pin=%s",(bacc,bpin))
        result=cursor.fetchone()
        print(result)
        mysql.commit()
        if result:
            return render_template ("balanceshow.html",acc=bacc,result=result)
    return "invalid"

@bank.route("/Deposit",methods=["POST","GET"])
def deposit():
    if request.method == "POST":
        dacc = request.form.get("accno")
        dpin = request.form.get("pin")
        damt = request.form.get("amt")
        cursor.execute("insert into statement (ant_no,pin,deposit) values(%s,%s,%s)",(dacc,dpin,damt))
        cursor.execute("update sign_up set deposit=(%s) where acc_no=%s and pin=%s",(damt,dacc,dpin))
        cursor.execute("update sign_up set balance=sign_up.balance+sign_up.deposit where acc_no=%s and pin=%s",(dacc,dpin))
        mysql.commit()
        return render_template("depshow.html",amt=damt)
    return render_template("deposit.html")


@bank.route("/Withdrawel",methods=["POST","GET"])
def withdrawel():
    if request.method == "POST":
        wacc=request.form.get("accno")
        wpin=request.form.get("pin")
        wamt=request.form.get("amount")
        cursor.execute("update sign_up set withdraw=(%s) where acc_no=%s and pin=%s",(wamt,wacc,wpin))
        cursor.execute("select balance from sign_up where balance>%s and acc_no=%s and pin=%s",(wamt,wacc,wpin))
        result=cursor.fetchone()
        mysql.commit()
        if result:
            cursor.execute("insert into statement (ant_no,pin,withdraw) values(%s,%s,%s)",(wacc,wpin,wamt))
            cursor.execute("update sign_up set balance=sign_up.balance-sign_up.withdraw where balance>%s and acc_no=%s and pin=%s",(wamt,wacc,wpin))
            return render_template("withshow.html",wamt=wamt)
        else:
            return render_template("withelse.html")
    return render_template("withdrawel.html")

@bank.route("/Mini Statement",methods=["POST","GET"])
def mini_statement():
    if request.method == "POST":
        macc = request.form.get("acc")
        mpin = request.form.get("pin")
        cursor.execute("select ant_no,deposit,withdraw from statement where ant_no=%s and pin=%s",(macc,mpin))
        reslt = cursor.fetchall()
        mysql.commit()
        if reslt:
            return render_template("minishow.html",reslt=reslt)
    return render_template("mini_statement.html")
@bank.route("/Logout",methods=["POST","GET"])
def logout():
    if request.method == "POST":
        mail = request.form.get("email")
        return render_template("loutshow.html",mail=mail)
    return render_template("logout.html")
    
@bank.route("/Signout",methods=["POST","GET"])
def signout():
    if request.method == "POST":
        mail = request.form.get("email")
        ps=request.form.get("password")
        cursor.execute("delete from sign_up where email=%s and password=%s",(mail,ps))
        mysql.commit()
        return render_template("soutshow.html",mail=mail)
    return render_template("signout.html")

if __name__ == "__main__":
    bank.run(debug=True)

cursor.close()
mysql.close()