INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Maijunen', 'scrypt:32768:8:1$QYw1LIh6jCzaM6Za$f7e0da749a5155e77b368a82a163e503c145cdbe73e91c7426df883571e8372355332d02fa4a69afe0a92cdbcfabdb01fa83ee07f93d6b5441223713333d64f5'
, 'Maija', '1', 'Moi oon Maija ja olen hauki');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Joo', 'scrypt:32768:8:1$QYw1LIh6jCzaM6Za$f7e0da749a5155e77b368a82a163e503c145cdbe73e91c7426df883571e8372355332d02fa4a69afe0a92cdbcfabdb01fa83ee07f93d6b5441223713333d64f5
', 'Joonas', '3', 'gucci laif and all things topology');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Ei', 'scrypt:32768:8:1$QYw1LIh6jCzaM6Za$f7e0da749a5155e77b368a82a163e503c145cdbe73e91c7426df883571e8372355332d02fa4a69afe0a92cdbcfabdb01fa83ee07f93d6b5441223713333d64f5
', 'Enja', '2', 'Emt miks oon tääl');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Jaa', 'scrypt:32768:8:1$QYw1LIh6jCzaM6Za$f7e0da749a5155e77b368a82a163e503c145cdbe73e91c7426df883571e8372355332d02fa4a69afe0a92cdbcfabdb01fa83ee07f93d6b5441223713333d64f5
', 'Mato', '1', 'Haluuks opiskella yhes?');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Hensku', 'scrypt:32768:8:1$QYw1LIh6jCzaM6Za$f7e0da749a5155e77b368a82a163e503c145cdbe73e91c7426df883571e8372355332d02fa4a69afe0a92cdbcfabdb01fa83ee07f93d6b5441223713333d64f5
', 'Henna', '1', 'Mitä jos halattais gurleffas?');


INSERT INTO likes (liker_id, likee_id) VALUES (1, 2);
INSERT INTO likes (liker_id, likee_id) VALUES (1, 3);
INSERT INTO likes (liker_id, likee_id) VALUES (1, 4);
INSERT INTO likes (liker_id, likee_id) VALUES (1, 5);


INSERT INTO likes (liker_id, likee_id) VALUES (2, 1);
INSERT INTO likes (liker_id, likee_id) VALUES (2, 4);
INSERT INTO likes (liker_id, likee_id) VALUES (2, 5);

INSERT INTO likes (liker_id, likee_id) VALUES (3, 1);

INSERT INTO likes (liker_id, likee_id) VALUES (4, 1);
INSERT INTO likes (liker_id, likee_id) VALUES (4, 5);

INSERT INTO likes (liker_id, likee_id) VALUES (5, 1);
INSERT INTO likes (liker_id, likee_id) VALUES (5, 2);

INSERT INTO user_orientations (user_id, orientation_id) VALUES (1, 5);
INSERT INTO user_orientations (user_id, orientation_id) VALUES (1, 6);