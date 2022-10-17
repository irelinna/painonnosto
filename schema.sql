CREATE TABLE workouts (
    id SERIAL PRIMARY KEY, 
    content TEXT,
    movement_id INTEGER REFERENCES movements,
    user_id INTEGER REFERENCES users
    );

CREATE TABLE movements (
    id SERIAL PRIMARY KEY, 
    content TEXT, 
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
    id SERIAL PRIMARY KEY,
    total_weight INTEGER,
    workout_id INTEGER REFERENCES workouts
    );

CREATE TABLE movements_in_workout(
    workout_id SERIAL PRIMARY KEY REFERENCES workouts,
    movement_id INTEGER REFERENCES movements
    );