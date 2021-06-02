FROM python:3.9.5-buster
WORKDIR /app
COPY python/requirements.txt requirements.txt
RUN apt-get update && apt-get -y install cmake
RUN pip3 install -r requirements.txt
ENV FLASK_APP webinterface
COPY . .
CMD ["python3", "test_suite.py"]