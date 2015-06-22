from rest_framework import status
from rest_framework.test import APITestCase


class CoreTests(APITestCase):
    def test_v1_tts_post_google(self):
        """
        Ensure we can send a message to tts
        """
        url = '/api/v1/core/tts/'
        data = {'message': u'bonjour', 'lang': 'en', 'driver': 'google'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_v1_tts_post_pico(self):
        """
        Ensure we can send a message to tts
        """
        url = '/api/v1/core/tts/'
        data = {'message': u'bonjour', 'lang': 'en', 'driver': 'pico'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_tts_get_google(self):
        """
        Ensure we can send a message to tts
        """
        url = '/api/v1/core/tts/'
        data = {'message': u'bonjour', 'lang': 'en', 'driver': 'google'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_tts_get_pico(self):
        """
        Ensure we can send a message to tts
        """
        url = '/api/v1/core/tts/'
        data = {'message': u'bonjour', 'lang': 'en', 'driver': 'pico'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_v1_tts_bad_request(self):
        """
        Ensure parameters are mandatory
        """
        url = '/api/v1/core/tts/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
