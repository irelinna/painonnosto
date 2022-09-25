CREATE TABLE workouts (id SERIAL PRIMARY KEY, content TEXT);

CREATE TABLE movements (id SERIAL PRIMARY KEY, content TEXT, workout_id INTEGER REFERENCES workouts);

