CREATE USER dockerservice with superuser password 'password';
CREATE DATABASE libraries_status;
GRANT ALL PRIVILEGES ON DATABASE libraries_status TO dockerservice;