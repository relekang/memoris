import redis

from flask import Flask, request

from utils import json_response

app = Flask(__name__)


@app.route('/<key>')
def api(key):
    r = redis.Redis()
    if request.method == 'POST':
        r.set(key, request.args.get('value'))

    value = r.get(key)
    if not value:
        return json_response({'error': 'No value for given key'}, 404)

    return json_response({
        key: value
    })

if __name__ == '__main__':
    app.run(debug=True)
