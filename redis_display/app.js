"use strict"

var redis = require('redis');

var express = require('express');
var app = express();

var client = redis.createClient({"host": process.env.REDIS_HOST || "redis"});
client.on('connect', () => {
   console.log("Connected");
});
client.on('error', (err) => {
   if(err)
      console.error(err);
});
app.get('/', (req,res) => {
  client.incr("node_temp", (err) => {
   client.get("node_temp", (err, val) => {
      if(err) { console.log(err); return res.end(); }

      res.write(val);
      res.end();
   });
  });
});

app.listen(9000, () => {
   console.log("Listening")
});
