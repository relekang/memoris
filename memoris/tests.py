import unittest
import json

import server


class TestViews(unittest.TestCase):

    EXISTS_VALUE = 'Yeah, I do'

    def setUp(self):
        self.app = server.app.test_client()
        self.redis = server.r
        self.redis.set('exists', self.EXISTS_VALUE)
        self.redis.hset('hexists', '1', self.EXISTS_VALUE)
        self.redis.hset('memoris:tokens', 'test', 'A user')

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEquals(response._status_code, 200)

    def test_get_api(self):
        r_existing = self.app.get('/exists?token=test')
        r_non_existing = self.app.get('/does-not-exists?token=test')
        self.assertEquals(r_existing._status_code, 200)
        self.assertEquals(
            json.loads(r_existing.data)['exists'],
            self.EXISTS_VALUE
        )
        self.assertEquals(r_non_existing._status_code, 404)

    def test_post_api(self):
        key = 'a-key'
        response = self.app.post('/%s?token=test' % key, data={
            'value': self.EXISTS_VALUE
        })
        self.assertEquals(response._status_code, 200)
        self.assertEquals(self.redis.get(key), self.EXISTS_VALUE)

    def test_get_hash_api(self):
        r_existing = self.app.get('/h/hexists?token=test')
        r_non_existing = self.app.get('/h/does-not-exists?token=test')
        self.assertEquals(r_existing._status_code, 200)
        self.assertEquals(
            json.loads(r_existing.data)['hexists']['1'],
            self.EXISTS_VALUE
        )
        self.assertEquals(r_non_existing._status_code, 404)

    def test_post_hash_api(self):
        name = 'a-name'
        key = 'a-key'
        response = self.app.post('/h/%s/%s?token=test' % (name, key), data={
            'value': self.EXISTS_VALUE
        })
        self.assertEquals(response._status_code, 200)
        self.assertEquals(self.redis.hget(name, key), self.EXISTS_VALUE)

    def test_require_token(self):
        response = self.app.get('/key')
        self.assertEquals(response._status_code, 403)

if __name__ == '__main__':
    unittest.main()
