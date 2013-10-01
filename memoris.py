import redis

from flask import Flask, request, render_template

from utils import json_response

app = Flask(__name__)

try:
    from local import local_config
    app.config.update(local_config)
except ImportError:
    print "Could not import local config"

r = redis.Redis(db=app.config['REDIS_DB'])


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

if __name__ == '__main__':
    app.run()
