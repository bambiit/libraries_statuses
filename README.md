# libraries_statuses

Heroku address: https://stormy-brushlands-78848.herokuapp.com/

Step 1: Start postgresql
docker build -t library_status_postgresql db/
docker run --network creaktor --rm --name postgresql -p 5432:5432 -it library_status_postgresql

Step 2: Start webapp
docker build -t library_status_web .
docker run --network creaktor --rm --name webapp -p 8000:8000 -e PORT=8000 -e DATABASE_URL=postgresql://dockerservice:password@postgresql:5432/libraries_status -it library_status_web

Step 3: Go to browser with 0.0.0.0:8000