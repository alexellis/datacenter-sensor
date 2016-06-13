import os
from flask import Flask, request, render_template
import redis
from reporter import Reporter

import json

host = os.getenv("REDIS_HOST")
if(host == None):
    host = "redis"

app = Flask(__name__)
cache = {}
last_members = []
r = Reporter(host, 6379)

def build_cache(cache):
    global last_members

    members = r.find_members()
    if(len(last_members) != len(members)):
        cache.clear()

    for member in members:
        cache[member]= {}
        cache[member]["temp"] = r.get_key(member + ".temp")
        cache[member]["temp.baseline"] = r.get_key(member + ".temp.baseline")
        cache[member]["motion"] = r.get_key(member + ".motion")
    last_members = members

@app.route('/', methods=['GET'])
def home():
    build_cache(cache)
    return json.dumps({"sensors": cache})

if __name__ == '__main__':
    print("0.0.0.0")
    app.run(debug=True, host='0.0.0.0')

