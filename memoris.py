import redis

from flask import Flask, request, render_template

from utils import json_response
from config import CONFIG

app = Flask(__name__)

app.config.update(CONFIG)

r = redis.Redis(
    db=app.config['REDIS_DB'],
    host=app.config['REDIS_HOST'],
    port=app.config['REDIS_PORT']
)


@app.route('/')
def index():
    return render_template('index.jinja2')


@app.route('/<key>')
def get_api(key):
    value = r.get(key)
    if not value:
        return json_response({'error': 'No value for given key'}, 404)

    return json_response({
        key: value
    })


@app.route('/<key>', methods=['POST'])
def post_api(key):
    if request.method == 'POST':
        r.set(key, request.values.get('value'))

    value = r.get(key)

    return json_response({
        key: value
    })


@app.route('/h/<name>')
def get_hash_all_api(name):
    return get_hash_api(name)


@app.route('/h/<name>/<key>')
def get_hash_api(name, key=None):
    if key is None:
        value = r.hgetall(name)
    else:
        value = {key: r.hget(name, key)}
    if not value:
        return json_response({'error': 'No value for given key'}, 404)

    return json_response({
        name: value
    })


@app.route('/h/<name>/<key>', methods=['POST'])
def post_hash_api(name, key):
    if request.method == 'POST':
        r.hset(name, key, request.values.get('value'))

    value = r.hget(name, key)

    return json_response({
        key: value
    })


if __name__ == '__main__':
    app.run()
