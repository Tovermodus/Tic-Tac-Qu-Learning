docker build -t tic-tac-qu-flask-test -f docker/FlaskImage/Dockerfile .
docker rm composetest_db_1
docker image rm tic-tac-qu-postgres
docker build --no-cache -t tic-tac-qu-postgres -f docker/PostgresDBImage/Dockerfile .
docker-compose -f docker/ComposeTest/docker-compose.yml up --exit-code-from flask
