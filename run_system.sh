docker build -t tic-tac-qu-flask-system -f docker/FlaskRunImage/Dockerfile .
docker build -t tic-tac-qu-postgres -f docker/PostgresDBImage/Dockerfile .
docker-compose -f docker/ComposeSystem/docker-compose.yml up