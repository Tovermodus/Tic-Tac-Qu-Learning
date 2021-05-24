FROM python:3.9.5-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get -y install cmake
RUN pip3 install -r requirements.txt
COPY . .
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]