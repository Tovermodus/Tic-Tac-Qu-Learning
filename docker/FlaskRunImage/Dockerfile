FROM python:3.9.5-buster
WORKDIR /app
COPY python/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV DB_USERNAME=admin
ENV DB_PASSWD=secret
ENV DB_SERVER=db
ENV DB_PORT=5432
ENV DB_NAME=docker

COPY . .
WORKDIR /app/python
CMD ["python3","flask_run.py"]