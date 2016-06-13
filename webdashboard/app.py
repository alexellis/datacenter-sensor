import os
from flask import Flask, request, render_template
import redis
from reporter import Reporter

import json

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
        item["temp"] = r.get_key(member + ".temp")
        item["temp.baseline"] = r.get_key(member + ".temp.baseline")
        item["motion"] = r.get_key(member + ".motion")
        cache.append(item)
    return cache

@app.route('/json', methods=['GET'])
def home_json():
    cache = build_cache()
    return json.dumps({"sensors": cache})

@app.route('/', methods=['GET'])
def home():
    hosts = build_cache()
    return render_template("nodes.html", hosts=hosts)

if __name__ == '__main__':
    print("0.0.0.0")
    app.run(debug=True, host='0.0.0.0')

