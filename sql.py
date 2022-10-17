from db import db
from flask import request


def add_movement(content,series,reps,kilos):
    sql = "INSERT INTO movements (content,series,reps,kilos) VALUES (:content,:series,:reps,:kilos)"
    db.session.execute(sql, {"content":content,"series":series,"reps":reps,"kilos":kilos})
    db.session.commit()

def add_workout(movements):
    for movement in movements:
        movement_id = movement.id
        sql = "INSERT INTO workouts (movement_id) VALUES (:movement_id)"
        db.session.execute(sql, {"movement_id":movement_id})
        db.session.commit()

def list_movements():
    result = db.session.execute("SELECT * FROM movements")
    movements = result.fetchall()
    return movements

def list_movements_by_workout(workouts):
    workout_id = workouts.id
    sql = "SELECT * FROM movements_in_workout, workouts WHERE movements_in_workout.workout_id = (:workout_id)"
    result = db.session.execute(sql, {"workout_id":workout_id})
    movements = result.fetchall()
    return movements


def list_workouts():
    result = db.session.execute("SELECT * FROM workouts")
    workouts = result.fetchall()
    return workouts


def get_movement_name(movement_id):
    sql = "SELECT content FROM movements WHERE movements.id = (movement_id)"
    result = db.session.execute(sql,{"movement_id":movement_id})
    movement_name = result.fetchone()
    return movement_name

def add_movement_to_workout(movement_name):
    sql = "INSERT INTO workouts (movement_id) VALUES (:id) SELECT id FROM movements WHERE movements.content = (:movement_name)"
    db.session.execute(sql, {"movement_name":movement_name})
    db.session.commit()

def add_workout_name(name):
    sql = "INSERT INTO workouts (content) VALUES (:name)"
    db.session.execute(sql, {'name':name})
    db.session.commit()

def get_workout_name(id):
    sql = "SELECT content FROM workouts WHERE id = (:id)"
    result = db.session.execute(sql, {'id':id})
    workout_name = result.fetchone()
    return workout_name

def get_workout_id(name):
    sql = "SELECT id FROM workouts WHERE content = (:name)"
    result = db.session.execute(sql, {'name':name})
    workout_id = result.fetchone()
    return workout_id


