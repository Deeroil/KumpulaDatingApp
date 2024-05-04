INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Maijunen', 'scrypt:32768:8:1$QYw1LIh6jCzaM6Za$f7e0da749a5155e77b368a82a163e503c145cdbe73e91c7426df883571e8372355332d02fa4a69afe0a92cdbcfabdb01fa83ee07f93d6b5441223713333d64f5', 'Maija', '1', 'Moi oon Maija ja olen hauki');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Joo', 'scrypt:32768:8:1$SwdW1Qpof91LuB10$81abb03f9f661009b0d2f39f269bf58855a9e295108ec338b059cc5e3c4b59c59b0cdceaa601552d4191d5b05feb3fad4bb310c473a4326de9c54f6ee9541b70', 'Joonas', '2', 'gucci laif and all things topology');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Enjukka', 'scrypt:32768:8:1$WFY9cHp7OmwaOveZ$9bc88d9a94ebaa1cb7c269af5b9d2407f891579c3da0029a5f4ae55e039089a34c4cb2beaa5c6552e95f9f490811cab08169be62e72b229f942e4f03c6c51cc5', 'Enja', '2', 'Emt miks oon tääl');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Matala', 'scrypt:32768:8:1$DhrryiUSQE4eRAcm$70d808a1f428c8d41f5293303703aca050b67b9102ebfdf6056ac7a86138c62c6703ae14fe5843cd57f5c1c723f25380e667c0e9ee7777fbccedd8daf6b16554', 'Mato', '1', 'Haluuks opiskella yhes?');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Hensku', 'scrypt:32768:8:1$9jSqO6QnpZX5V1SU$d5087cf7fc7af1d1153c297b86d63cfaf3218b5c3553da884305fee835f977acca21b5011e05a308f50193e756e971fe5d03b28995ef50ce0966d1286a1445fc', 'Henna', '1', 'Mitä jos halailtais gurleffas?');
INSERT INTO users (username, passw, name, studyfield_id, bio) VALUES ('Fyysikko', 'scrypt:32768:8:1$DqMxRZWgHV34oGHW$312e9368101449699ca0a6b9f18302380d58c32a2c041afe179301c381ebc7f9a0735d6b76a05e069069f3ea3f40d8473a991e9aecd6fad201d5eafb288480ea', 'Andrew', '3', 'My love language is physical touch HEHHEH');

INSERT INTO likes (liker_id, likee_id) VALUES (1, 2);
INSERT INTO likes (liker_id, likee_id) VALUES (1, 3);
INSERT INTO likes (liker_id, likee_id) VALUES (1, 4);
INSERT INTO likes (liker_id, likee_id) VALUES (1, 5);
INSERT INTO likes (liker_id, likee_id) VALUES (1, 6);

INSERT INTO likes (liker_id, likee_id) VALUES (2, 1);
INSERT INTO likes (liker_id, likee_id) VALUES (2, 4);
INSERT INTO likes (liker_id, likee_id) VALUES (2, 5);

INSERT INTO likes (liker_id, likee_id) VALUES (3, 1);

INSERT INTO likes (liker_id, likee_id) VALUES (4, 1);
INSERT INTO likes (liker_id, likee_id) VALUES (4, 5);

INSERT INTO likes (liker_id, likee_id) VALUES (5, 1);
INSERT INTO likes (liker_id, likee_id) VALUES (5, 2);

INSERT INTO likes (liker_id, likee_id) VALUES (6, 1);


INSERT INTO user_orientations (user_id, orientation_id) VALUES (1, 4);
INSERT INTO user_orientations (user_id, orientation_id) VALUES (1, 7);

INSERT INTO user_orientations (user_id, orientation_id) VALUES (2, 2);
INSERT INTO user_orientations (user_id, orientation_id) VALUES (2, 12);

INSERT INTO user_orientations (user_id, orientation_id) VALUES (3, 4);
INSERT INTO user_orientations (user_id, orientation_id) VALUES (3, 13);

INSERT INTO user_orientations (user_id, orientation_id) VALUES (5, 3);

INSERT INTO user_orientations (user_id, orientation_id) VALUES (6, 4);
INSERT INTO user_orientations (user_id, orientation_id) VALUES (6, 8);
INSERT INTO user_orientations (user_id, orientation_id) VALUES (6, 13);