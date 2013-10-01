import redis

from flask import Flask, request, render_template

from utils import json_response

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.jinja2')


@app.route('/<key>')
def get_api(key):
    r = redis.Redis()
    value = r.get(key)
    if not value:
        return json_response({'error': 'No value for given key'}, 404)

    return json_response({
        key: value
    })


@app.route('/<key>', methods=['POST'])
def post_api(key):
    r = redis.Redis()
    if request.method == 'POST':
        r.set(key, request.values.get('value'))

    value = r.get(key)

    return json_response({
        key: value
    })

if __name__ == '__main__':
    app.run()
