FROM python:3.9.5-buster
WORKDIR /app
COPY python/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP webinterface
ENV FLASK_APP webinterface
ENV FLASK_APP webinterface
ENV DATABASE_URL="postgresql://localhost/flask_api"
COPY . .
WORKDIR /app/python
CMD ["flask", "run", "--host=0.0.0.0"]