from rest_framework import status
from rest_framework.test import APITestCase


class CoreTests(APITestCase):
    def test_v1_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/core/intents/'
        data = {
            'name': u'plugin_test_add',
            'method': u'POST',
            'api_url': u'/api/v1/plugin-test/add/',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))
