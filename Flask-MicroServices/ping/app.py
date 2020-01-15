from flask import Flask, jsonify
from pythonping import ping
import time, json
from influxdb import InfluxDBClient
import os, requests


pingService = Flask(__name__)

def config():
    with open("./config") as conf:
        config = json.load(conf)
    return config

# def get_conf():
#     response = requests.get("http://127.0.0.1:8000/api/pings")
#     return response

@pingService.route("/ping")
def main():
    
    # result = get_conf()
    # if result.status_code == 200:
    #     targets = result.json()[0]['ip_target']
    #     interval = result.json()[0]['interval']
    # else:
    #     targets = None
    #     interval = None

    targets = config()["TARGETS"]
    interval = config()["INTERVAL"]

    while True:
        if not (targets is None and interval is None):
            for target in targets:
                try:
                    response = ping(target)
                    if response.success:
                        db_storage(target, response.rtt_avg_ms)               
                        #return jsonify(ping_target=target, rtt_avg_ms=response.rtt_avg_ms)
                except Exception as e:
                    print(e)
            time.sleep(interval)
    
            
#Change 'localhost' to 'influxdb' and 'influx_metrics' to 'metrics_collect' before pushing to git
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