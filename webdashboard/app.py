import os
import redis
import json

from flask import Flask, request, render_template, send_from_directory
from reporter import Reporter

host = os.getenv("REDIS_HOST")
if(host == None):
    host = "redis"

app = Flask(__name__)
r = Reporter(host, 6379)

def build_cache():
    cache = []
    members = r.find_members()

    for member in members:
        item = {}
        item["name"] = member
        item["temp"] = float( r.get_key(member + ".temp") )
        item["temp.baseline"] = float( r.get_key(member + ".temp.baseline") )
        item["motion"] = float( r.get_key(member + ".motion") )
        try:
            item["temp.diff"] = float( round(abs(float(item["temp"]) - float(item["temp.baseline"])), 2) )
            cache.append(item)
        except:
            print("oops " + member + "has bad data")
    return cache

@app.route('/json', methods=['GET'])
def home_json():
    cache = build_cache()
    return json.dumps({"sensors": cache})

@app.route('/nodes/', methods=['GET'])
def home():
    hosts = build_cache()
    return render_template("nodes.html", hosts=hosts)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/', methods=['GET'])
def sensors():
    return render_template("sensors.html")

if __name__ == '__main__':
    print("0.0.0.0")
    app.run(debug=True, host='0.0.0.0')
