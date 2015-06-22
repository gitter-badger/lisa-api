from rest_framework import status
from rest_framework.test import APITestCase
from lisa_api.api.models import Zone


class CoreTests(APITestCase):
    def setUp(self):
        self.zone_bathroom = Zone.objects.create(name="bathroom")
        self.zone_bathroom_url = '/api/v1/core/zones/%i/' % self.zone_bathroom.id

    def test_v1_create_client(self):
        """
        Ensure we can create a new client object.
        """
        url = '/api/v1/core/clients/'
        data = {
            'name': u'rpi-bathroom',
            'mac': u'00:11:22:33:44:55',
            'zone': [self.zone_bathroom_url]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('name'), data.get('name'))
