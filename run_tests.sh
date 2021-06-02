docker build -t tic-tac-qu-flask-test -f docker/FlaskImage/Dockerfile .
docker build -t tic-tac-qu-postgres -f docker/PostgresDBImage/Dockerfile .
docker-compose -f docker/ComposeTest/docker-compose.yml up --exit-code-from flask
