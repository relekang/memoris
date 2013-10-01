CONFIG = {
    'REDIS_DB': 1,
    'REDIS_HOST': '127.0.0.1',
    'REDIS_PORT': 6379
}

try:
    from local import local_config
    CONFIG.update(local_config)
except ImportError:
    print "Could not import local config"
