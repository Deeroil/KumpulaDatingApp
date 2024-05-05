
CREATE TABLE studyfields (
  id SERIAL PRIMARY KEY,
  field TEXT UNIQUE
);

INSERT INTO studyfields (field) VALUES ('Computer Science');
INSERT INTO studyfields (field) VALUES ('Math');
INSERT INTO studyfields (field) VALUES ('Physics');

CREATE TABLE orientations (
  id SERIAL PRIMARY KEY,
  orientation TEXT UNIQUE
  );

INSERT INTO orientations (orientation) VALUES ('Gay');
INSERT INTO orientations (orientation) VALUES ('Bi');
INSERT INTO orientations (orientation) VALUES ('Pan');
INSERT INTO orientations (orientation) VALUES ('Queer');
INSERT INTO orientations (orientation) VALUES ('Straight');
INSERT INTO orientations (orientation) VALUES ('Asexual');
INSERT INTO orientations (orientation) VALUES ('Aromantic');
INSERT INTO orientations (orientation) VALUES ('Demisexual');
INSERT INTO orientations (orientation) VALUES ('Demiromantic');
INSERT INTO orientations (orientation) VALUES ('Kinky');
INSERT INTO orientations (orientation) VALUES ('Vanilla');
INSERT INTO orientations (orientation) VALUES ('Polyamorous');
INSERT INTO orientations (orientation) VALUES ('Non-mono');
INSERT INTO orientations (orientation) VALUES ('Mono');

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE,
  passw TEXT,
  name TEXT,
  studyfield_id INTEGER REFERENCES studyfields,
  bio TEXT
);

CREATE TABLE user_orientations (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  orientation_id INTEGER REFERENCES orientations(id),
  UNIQUE (user_id, orientation_id)
);

CREATE TABLE likes (
  id SERIAL PRIMARY KEY,
  liker_id INTEGER REFERENCES users,
  likee_id INTEGER REFERENCES users,
  UNIQUE (liker_id, likee_id)
);
