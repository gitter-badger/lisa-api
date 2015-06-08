from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Group


class CoreTests(APITestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.group = Group.objects.create(name="testgroupadmin")
        self.group_url = '/api/v1/core/groups/%i/' % self.group.id

    def test_v1_create_user(self):
        """
        Ensure we can create a new user object.
        """
        url = '/api/v1/core/users/'
        data = {
            'username': u'testuser',
            'first_name': u'user',
            'last_name': u'test',
            'email': u'test@lisa-project.net',
            'groups': [self.group_url]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('username'), data.get('username'))
