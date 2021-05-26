FROM python:3.9.5-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get -y install cmake
RUN pip3 install -r requirements.txt
ENV FLAK_APP webinterface
COPY . .
CMD ["python3", "test_suite.py"]