from rest_framework import status
from rest_framework.test import APITestCase


class CoreTests(APITestCase):
    def test_v1_create_group(self):
        """
        Ensure we can create a new group object.
        """
        url = '/api/v1/core/groups/'
        data = {'name': u'testgroup'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))
