DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INT PRIMARY KEY,
    username VARCHAR(225) NOT NULL,
    email VARCHAR(225),
    created_at DATETIME
);

CREATE TABLE posts (
    post_id INT PRIMARY KEY,
    user_id INT,
    title VARCHAR(225),
    body TEXT,
    posted_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

INSERT INTO users VALUES (1,'andy','andy@example.com','2026-01-00 10:00:00');
INSERT INTO users VALUES (2,'ben','ben@example.com','2026-01-02 11:00:00');
INSERT INTO users VALUES (3,'steve','steve@example.com','2026-01-05 12:00:00');
INSERT INTO users VALUES (4,'alex','alex@example.com','2026-01-04 13:00:00');
INSERT INTO users VALUES (5,'ethan','ethan@example.com','2026-01-06 14:00:00');
INSERT INTO users VALUES (6,'frank','frank@example.com','2026-01-03 15:00:00');
INSERT INTO users VALUES (7,'joe','joe@example.com','2026-01-07 16:00:00');
INSERT INTO users VALUES (8,'james','james@example.com','2026-01-08 17:00:00');
INSERT INTO users VALUES (9,'jose','jose@example.com','2026-01-01 18:00:00');
INSERT INTO users VALUES (10,'judy','judy@example.com','2026-01-10 19:00:00');

INSERT INTO posts VALUES (1,1,'Hello world','My first post','2026-02-01 09:00:00');
INSERT INTO posts VALUES (2,1,'SQL is fun','Learning joins','2026-02-02 09:00:00');
INSERT INTO posts VALUES (3,2,'Coffee','Best morning drink','2026-02-03 09:00:00');
INSERT INTO posts VALUES (4,3,'Travel','Trip to Italy','2026-02-04 09:00:00');
INSERT INTO posts VALUES (5,4,'Books','What I am reading','2026-02-05 09:00:00');
INSERT INTO posts VALUES (6,5,'Music','Favorite albums','2026-02-06 09:00:00');
INSERT INTO posts VALUES (7,6,'Fitness','Gym routine','2026-02-07 09:00:00');
INSERT INTO posts VALUES (8,7,'Cooking','Pasta recipe','2026-02-08 09:00:00');
INSERT INTO posts VALUES (9,8,'Gaming','Top games','2026-02-09 09:00:00');
INSERT INTO posts VALUES (10,9,'Movies','Weekend watchlist','2026-02-10 09:00:00');
INSERT INTO posts VALUES (11,10,'Pets','My dog','2026-02-11 09:00:00');