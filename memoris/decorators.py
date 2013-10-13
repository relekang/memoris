from functools import wraps
from flask import request

from utils import json_response


def require_token():
    from server import r as redis

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            token = request.values.get('token')
            if token is None and not token in redis.hgetall('memoris:tokens'):
                return json_response({'error': 'Token required'}, status=400)
            return func(*args, **kwargs)
        return wrapped
    return wrapper
