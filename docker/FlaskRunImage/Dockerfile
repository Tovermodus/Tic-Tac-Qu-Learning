FROM python:3.9.5-buster
WORKDIR /app
COPY python/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP=webinterface
ENV DB_USERNAME=admin
ENV DB_PASSWD=secret
ENV DB_SERVER=db
ENV DB_PORT=5432
ENV DB_NAME=docker

COPY . .
WORKDIR /app/python
CMD ["flask", "run", "--host=0.0.0.0"]