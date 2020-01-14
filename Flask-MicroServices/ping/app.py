from flask import Flask
from pythonping import ping
import time, json
from influxdb import InfluxDBClient
import os


pingService = Flask(__name__)

def config():
    with open("./config") as conf:
        config = json.load(conf)
    return config

@pingService.route("/ping")
def main():
    targets = config()["TARGETS"]
    interval = config()["INTERVAL"]
    while True:
        for target in targets:
            try:
                response = ping(target)
                if response.success:
                    db_storage(target, response.rtt_avg_ms)               
                    #return jsonify(ping_target=target, rtt_avg_ms=response.rtt_avg_ms)
            except Exception as e:
                print(e)
        time.sleep(interval)
            
        
def db_storage(target,rtt_avg):
    db = InfluxDBClient('influxdb', 8086, database='metrics_collect',username='user', password='userpass', ssl=False, verify_ssl=False)
    data = [
        {
            "measurement": "ping",
            "tags": {
                "target": target
            },
            "fields": {
                "rtt_avg": rtt_avg
            }
        }
    ]
    db.write_points(data)


if __name__ == "__main__":
    pingService.run(debug=True)