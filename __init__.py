from flask import Flask, request
from flask_restful import Resource, Api
import redis
import json

app = Flask(__name__)
api = Api(app)

r = redis.StrictRedis(charset="utf-8", decode_responses=True)

app_data = ['amigo']

@app.route('/log/<lname>', methods=['GET', 'POST'])
def doit(lname):
    bucket = "log_"+lname
    if request.method == 'POST':
        r.lpush(bucket, request.data)
        r.ltrim(bucket, 0, 99)

    out = '\n'.join(r.lrange(bucket, 0, 99))
    return out, 200, {'Content-Type': 'text/plain'}


if __name__ == '__main__':
    app.run(debug=False)