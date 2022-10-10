from db import db
from flask import request

def add_movement(content,series,reps,kilos):
    sql = "INSERT INTO movements (content,series,reps,kilos) VALUES (:content,:series,:reps,:kilos)"
    db.session.execute(sql, {"content":content,"series":series,"reps":reps,"kilos":kilos})
    db.session.commit()

def add_workout(workout):
    sql = "INSERT INTO workouts VALUES (:workout) SELECT FROM movements WHERE movements.workout_id = workouts.id"
    db.session.execute(sql, {"workout":workout})
    db.session.commit()

def list_movements():
    # result = db.session.execute("SELECT content FROM movements WHERE movements.creator_id = users.id")
    result = db.session.execute("SELECT * FROM movements")
    movements = result.fetchall()
    return movements

def list_workouts():
    result = db.session.execute("SELECT * FROM workouts")
    workouts = result.fetchall()
    return workouts

def check_username():
    check1 = "SELECT username FROM users WHERE "
    username = request.form["username"]

def add_numbers():
    sql = "INSERT INTO numbers VALUES (:series"

def list_specific_workout():
    #todo: listing by workout number(from previous workouts-page)
    pass
