from rest_framework import status
from rest_framework.test import APITestCase
from lisa_api.lisa.configuration import CONF as config


class CoreTests(APITestCase):
    def setUp(self):
        super(CoreTests, self).setUp()
        config.add_opt(name='user', value='guest', section='rabbitmq')
        config.add_opt(name='password', value='guest', section='rabbitmq')
        config.add_opt(name='host', value='localhost', section='rabbitmq')

    def test_v1_speak(self):
        """
        Ensure we can send a message to rabbitmq
        """
        url = '/api/v1/core/speak/'
        data = {'message': u'test', 'zone': u'test', 'source': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)