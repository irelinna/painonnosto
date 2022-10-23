CREATE TABLE workouts (
    id SERIAL PRIMARY KEY, 
    workout_name TEXT,
    movement_id INTEGER REFERENCES movements,
    user_id INTEGER REFERENCES users
    );

CREATE TABLE movements (
    id SERIAL PRIMARY KEY, 
    movement_name TEXT, 
    series INTEGER,
    reps INTEGER,
    kilos FLOAT,
    creator_id INTEGER REFERENCES users
    );


CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
    );

CREATE TABLE stats (
    workout_id INTEGER REFERENCES workouts,
    total_weight INTEGER
    );

CREATE TABLE movements_in_workout(
    workout_id INTEGER REFERENCES workouts,
    movement_id INTEGER REFERENCES movements
    );