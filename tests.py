import unittest
import json

import memoris


class TestViews(unittest.TestCase):

    EXISTS_VALUE = 'Yeah, I do'

    def setUp(self):
        self.app = memoris.app.test_client()
        self.redis = memoris.r
        self.redis.set('exists', self.EXISTS_VALUE)

    def tearDown(self):
        pass

    def test_index(self):
        response = self.app.get('/')
        self.assertEquals(response._status_code, 200)

    def test_get_api(self):
        r_existing = self.app.get('/exists')
        r_non_existing = self.app.get('/does-not-exists')
        self.assertEquals(r_existing._status_code, 200)
        self.assertEquals(
            json.loads(r_existing.data)['exists'],
            self.EXISTS_VALUE
        )
        self.assertEquals(r_non_existing._status_code, 404)

    def test_post_api(self):
        key = 'a-key'
        response = self.app.post('/%s' % key, data={
            'value': self.EXISTS_VALUE
        })
        self.assertEquals(response._status_code, 200)
        self.assertEquals(self.redis.get(key), self.EXISTS_VALUE)

if __name__ == '__main__':
    unittest.main()
