CONFIG = {
    'REDIS_DB': 1,
    'REDIS_HOST': '127.0.0.1',
    'REDIS_PORT': 6379
}

try:
    from local import LOCAL_CONFIG
    CONFIG.update(LOCAL_CONFIG)
    print "\nConfig:\n--------\n%s\n" % CONFIG
except ImportError:
    print "Could not import local config"
