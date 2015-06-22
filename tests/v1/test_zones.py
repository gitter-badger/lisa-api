from rest_framework import status
from rest_framework.test import APITestCase


class CoreTests(APITestCase):
    def test_v1_create_zone(self):
        """
        Ensure we can create a new zone object.
        """
        url = '/api/v1/core/zones/'
        data = {'name': u'kitchen'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))
