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