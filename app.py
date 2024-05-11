from flask import Flask, render_template, request, session, redirect
import json
import psycopg2
app=Flask(__name__)
app.secret_key="abcd"

conn = psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="Postgres",
                        port="5432")



@app.route("/")
def home():
    if "email" not in session:
        session["email"]="dummy@gmail.com"
        session["password"]="dummy"
    return render_template("home.html")

@app.route("/signin", methods=["GET"])
def signin():
    return render_template("signin.html")

@app.route("/signup", methods=["GET"])
def signup():
    return render_template("signup.html")

@app.route("/signinsubmit", methods=["POST"])
def signinsubmit():
    data=request.form
    email=data.get("email")
    password=data.get("password")
    cursor=conn.cursor()
    cursor.execute(f"select * from login where email='{email}' and password='{password}'")
    row=cursor.fetchone()
    if row:
        session["name"]=row[2]
        session["email"]=email
        session["password"]=password
        return redirect("/")
    else:
        return redirect("/error")
    
@app.route("/error")
def error():
    return render_template("error.html")

@app.route("/signupsubmit", methods=["POST"])
def signupsubmit():
    data=request.form
    name=data.get("name")
    email=data.get("email")
    password=data.get("password")
    session["name"]=name
    session["email"]=email
    session["password"]=password
    cursor=conn.cursor()
    cursor.execute(f"insert into login(email,password,name) values('{email}','{password}','{name}')")
    conn.commit()
    return redirect("/")

@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
    
