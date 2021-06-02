FROM python:3.9.5-buster
WORKDIR /app
COPY python/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP webinterface
COPY . .
WORKDIR /app/python
CMD ["flask", "run", "--host=0.0.0.0"]