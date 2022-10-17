from app import app
from db import db
import sql
import users
from flask import url_for, render_template, redirect, abort, request, session


#todo: sivupohjat ja ulkonäkö, listaaminen treenin mukaan

@app.route("/", methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if request.form.get('register_button') == 'Register':
            return render_template('register.html')
        elif request.form.get('login_button') == 'Login':
            return render_template('login.html')
        else:
            pass
        
    elif request.method == 'GET':
        return render_template('index.html')

    return render_template('index.html')

@app.route("/frontpage", methods=['GET','POST'])
def frontpage():
    if request.method == 'POST':
        print(request)
        if request.form.get('new_workout') == 'New workout':
            return redirect('/workout_name')
            #return render_template('workout_name.html')
        elif request.form.get('previous_workout') == 'Previous workouts':
            return redirect('/previous')
        else:
            pass
    elif request.method == 'GET':
        return render_template('frontpage.html')

    return render_template('frontpage.html')



@app.route("/new", methods=['GET','POST'])
def new():
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        content = request.form["content"]
        series = request.form["series"]
        reps = request.form["reps"]
        kilos = request.form["kilos"]
        if (len(content) != 0):
            sql.add_movement(content,series,reps,kilos)
        else:
            return render_template("name_error")
        return redirect("/list")
    if request.method == 'GET':
        return render_template('new.html')

@app.route("/previous", methods=['GET','POST'])
def previous():
    if request.method == 'POST':
        return render_template('previous.html')
    if request.method == 'GET':
        workouts = sql.list_workouts()
        if request.form.get('workout_details') == 'Workout details':
            print(request)
            return redirect("/workout_list", name = workouts.content)
        return render_template('previous.html', workouts = workouts)


@app.route("/workout_list", methods=['GET','POST'])
def workout_list():
    if request.method == 'GET':
        print(request)
        workouts = sql.list_workouts()
        movements = sql.list_movements_by_workout(workouts)
        return render_template("workout_list.html", movements = movements)
    if request.method == 'POST':
        return render_template("workout_list.html")



@app.route("/workout_name", methods=['GET','POST'])
def workout_name():
    if request.method == 'POST':
        if request.form.get('start_workout') == 'Start workout':
            name = request.form['workout_name']
            if (len(name) != 0):
                sql.add_workout_name(name)
                return render_template('list.html', name = name)
            else:
                return render_template("name_error.html")
    if request.method == 'GET':
        return render_template('workout_name.html')


@app.route("/list", methods=['GET','POST'])
def list():
    if request.method == 'GET':
        print(request)
        movements = sql.list_movements()
        if request.form.get('add_to_workout') == 'Add movement to workout':
            movement_name = request.form.get["movement_name"]
            print(request)
            sql.add_movement_to_workout(movement_name)
        return render_template("list.html", movements = movements) 
    if request.method == 'POST':
        print(request)
        movements = sql.list_movements()
        if request.form.get('add_new_movement') == 'Add new movement':
            print(request)
            return redirect('/new')
        elif request.form.get('finish_workout') == 'Finish and save workout':
            sql.add_workout(movements)
            return redirect('/previous')
        



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            session["username"] = username
            return redirect("/frontpage")
        else:
            return render_template("error.html", message="Wrong username or password")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords don't match")
        if users.register(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Registering failed")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")