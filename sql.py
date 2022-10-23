from db import db
from flask import request


def add_movement(movement_name,series,reps,kilos):
    sql = "INSERT INTO movements (movement_name,series,reps,kilos) VALUES (:movement_name,:series,:reps,:kilos)"
    db.session.execute(sql, {"movement_name":movement_name,"series":series,"reps":reps,"kilos":kilos})
    db.session.commit()


def total_weight_in_movement(movement_id):
    id, = movement_id
    movement = get_movement_by_id(id)
    weight = movement.series*movement.reps*movement.kilos
    return weight

def total_weight(workout_id):
    sql = "SELECT total_weight FROM stats WHERE workout_id = (:workout_id)"
    result = db.session.execute(sql, {"workout_id":workout_id})
    return result
    

def insert_weight_to_stats(weight,workout_id):
    sql = "INSERT INTO stats (total_weight, workout_id) VALUES (:weight, :workout_id)"
    db.session.execute(sql, {"workout_id":workout_id,"weight":weight})
    db.session.commit()


def add_movement_id_to_workout(movement_id, workout_id):
    sql = "INSERT INTO movements_in_workout (workout_id, movement_id) VALUES (:workout_id, :movement_id)"
    db.session.execute(sql, {"workout_id":workout_id,"movement_id":movement_id})
    db.session.commit()

def get_movements_in_workout(workout_id):
    sql = "SELECT movement_id FROM movements_in_workout WHERE workout_id = (:workout_id)"
    result = db.session.execute(sql, {"workout_id":workout_id})
    return result.fetchall()


def list_workouts():
    result = db.session.execute("SELECT * FROM workouts")
    workouts = result.fetchall()
    return workouts


def get_movement_id(name):
    sql = "SELECT id FROM movements WHERE movement_name = (:name)"
    result = db.session.execute(sql, {'name':name})
    movement_id = result.fetchone()
    return movement_id


def get_movement_by_id(movement_id):
    sql = "SELECT * FROM movements WHERE id = (:movement_id)"
    result = db.session.execute(sql, {'movement_id':movement_id})
    movement = result.fetchone()
    return movement


def add_workout_name(name):
    sql = "INSERT INTO workouts (workout_name) VALUES (:name)"
    db.session.execute(sql, {'name':name})
    db.session.commit()


def get_workout(workout_id):
    sql = "SELECT * FROM workouts WHERE id = (:workout_id)"
    result = db.session.execute(sql, {'workout_id':workout_id})
    workout = result.fetchone()
    return workout

def get_workout_by_name(name):
    sql = "SELECT * FROM workouts WHERE workout_name = (:name)"
    result = db.session.execute(sql, {'name':name})
    workout = result.fetchone()
    return workout