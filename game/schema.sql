DROP TABLE IF EXISTS users;
CREATE TABLE users (
  id SERIAL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  inventory JSONB
);



