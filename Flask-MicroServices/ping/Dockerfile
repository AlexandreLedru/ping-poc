FROM python:3.6-alpine

# Add the dependancies here
RUN pip3 install pythonping Flask influxdb
ADD . /app
WORKDIR /app

CMD ["flask","run","--host=0.0.0.0"]