CREATE USER carniviews_user WITH PASSWORD 'secret';
CREATE DATABASE carniviews OWNER carniviews_user;
GRANT ALL PRIVILEGES ON DATABASE carniviews TO carniviews_user;