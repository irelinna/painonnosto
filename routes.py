from app import app
from db import db
import sql
import users
from flask import url_for, render_template, redirect, abort, request, session


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


@app.route('/frontpage', methods=['GET','POST'])
def frontpage():
    if request.method == 'GET':
        return render_template('frontpage.html')
    elif request.method == 'POST':
        if request.form.get('new_workout') == 'New workout':
            return redirect('/workout_name')
        elif request.form.get('previous_workout') == 'Previous workouts':
            return redirect('/previous')
        else:
            pass
    return render_template('frontpage.html')


@app.route("/new/<workout_id>", methods=['GET','POST'])
def new(workout_id):
    workout = sql.get_workout(workout_id)
    if request.method == 'POST':
        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)
        if request.form.get('add_movement') == "Add movement to workout":
            movement_name = request.form["movement_name"]
            series = request.form["series"]
            reps = request.form["reps"]
            kilos = request.form["kilos"]
            if (len(movement_name) != 0):
                sql.add_movement(movement_name,series,reps,kilos)
                created_movement_id, = sql.get_movement_id(movement_name)
                sql.add_movement_id_to_workout(created_movement_id, workout_id)
                return redirect(url_for('list', workout_id = workout_id))
            else:
                return render_template("error.html", message = "Invalid or empty name")
    if request.method == 'GET':
        return render_template('new.html', workout = workout)

@app.route("/previous", methods=['GET','POST'])
def previous():
    workouts = sql.list_workouts()
    if request.method == 'POST':
        if request.form.get('workout_id'):
            id = request.form.get('workout_id')
            return redirect(url_for('workout_list', workout_id = id))
    if request.method == 'GET':
        return render_template('previous.html',workouts = workouts)
        

@app.route('/workout_list/<workout_id>', methods=['GET','POST'])
def workout_list(workout_id):
    workout = sql.get_workout(workout_id)
    movements_in_workout = sql.get_movements_in_workout(workout_id)
    movements_list=[]
    total_weight = 0
    for movement in movements_in_workout:
        stripped_id, = movement
        weight = sql.total_weight_in_movement(movement)
        total_weight += weight
    sql.insert_weight_to_stats(total_weight,workout_id)
    if request.method == 'GET':
        for movement in movements_in_workout:
            stripped_id, = movement
            current_movement = sql.get_movement_by_id(stripped_id)
            movements_list.append(current_movement)
        return render_template("workout_list.html", workout = workout, movements = movements_list, stats = total_weight)
    if request.method == 'POST':
        if request.form.get('edit_workout'):
            return redirect(url_for("list", workout_id = workout_id))


@app.route("/list/<workout_id>", methods=['GET','POST'])
def list(workout_id):
    workout = sql.get_workout(workout_id)
    movements_in_workout = sql.get_movements_in_workout(workout_id)
    movements_list=[]
    total_weight = 0
    for movement in movements_in_workout:
        weight = sql.total_weight_in_movement(movement)
        total_weight += weight
    sql.insert_weight_to_stats(total_weight,workout_id)
    weight_in_workout = sql.total_weight(workout_id)
    if request.method == 'GET':
        for movement in movements_in_workout:
            stripped_id, = movement
            current_movement = sql.get_movement_by_id(stripped_id)
            movements_list.append(current_movement)
        return render_template("list.html", workout = workout, movements = movements_list, stats = weight_in_workout) 
    elif request.method == 'POST':
        render_template("list.html", workout =workout)
        workout = sql.get_workout(workout_id)
        if request.form.get('add_new_movement') == 'Add new movement':
            return redirect(url_for('new', workout_id = workout_id))
        elif request.form.get('finish_workout') == 'Finish and save workout':
            return redirect('/previous')
        return render_template("list.html", workout = workout, movements = movements_list, stats = weight_in_workout) 
        

@app.route("/workout_name", methods=['GET','POST'])
def workout_name():
    if request.method == 'POST':
        if request.form.get('start_workout') == 'Start workout':
            name = request.form['workout_name']
            if (len(name) != 0):
                sql.add_workout_name(name)
                created_workout = sql.get_workout_by_name(name)
                return redirect(url_for('list', workout_id = created_workout.id))
            else:
                return render_template("error.html", message = "Invalid or empty name")
    if request.method == 'GET':
        return render_template('workout_name.html')


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