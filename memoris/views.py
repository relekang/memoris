import redis

from flask import request, render_template

from utils import json_response


def index():
    return render_template('index.jinja2')


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
