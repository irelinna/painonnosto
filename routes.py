from app import app, session
from db import db
import users
from flask import render_template, redirect, request



@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form.get('new_workout') == 'Uusi treeni':
            return render_template('list.html')
        elif request.form.get('previous_workout') == 'Aikaisemmat treenit':
            return render_template('previous.html')
        else:
            pass
        
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template('index.html')



@app.route("/new", methods=['GET','POST'])
def new():
    if request.method == 'POST':
        content = request.form["content"]
        sql = "INSERT INTO movements (content) VALUES (:content)"
        db.session.execute(sql, {"content":content})
        db.session.commit()
        return redirect("/list")
    if request.method == 'GET':
        return render_template('new.html')


@app.route("/list", methods=['GET'])
def list():
    if request.method == 'GET':
        result = db.session.execute("SELECT content FROM movements")
        movements = result.fetchall()
        return render_template("list.html", movements=movements) 


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")