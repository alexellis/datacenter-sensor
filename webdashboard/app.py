from flask import Flask, request, render_template
import redis

import json

host = os.getenv("REDIS_HOST")
if(host == None):
    host = "redis"

app = Flask(__name__)
cache = {}
last_members = []

def build_cache():
    members = r.find_members()
    if(len(last_members) != len(members)):
        cache = {}

    last_members = members
    for member in members:
        cache[member]= {}
        cache[member]["temp"] = r.get_key(member + ".temp")
        cache[member]["temp.baseline"] = r.get_key(member + ".temp.baseline")
        cache[member]["motion"] = r.get_key(member + ".motion")

def on_sensor_data(channel, data):
    build_cache()

r.set_on_sensor_data(on_sensor_data)
r.subscribe()

@app.route('/', methods=['GET'])
def home():
    return json.dumps({"sensors": cache})
