from rest_framework import status
from rest_framework.test import APITestCase
import responses
import re


class CoreTests(APITestCase):
    @responses.activate
    def test_v1_tts_post_google(self):
        """
        Ensure we can send a message to tts
        """
        url_re = re.compile(r'https?://translate.google.com/translate_tts\.*')
        responses.add(responses.GET, url_re,
                      body='DATAMP3', status=200,
                      content_type='audio/mpeg')

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

    def test_v1_tts_post_pico_other_lang(self):
        """
        Ensure we can send a message to tts
        """
        url = '/api/v1/core/tts/'
        data = {'message': u'bonjour', 'lang': 'fr', 'driver': 'pico'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @responses.activate
    def test_v1_tts_get_google(self):
        """
        Ensure we can send a message to tts
        """
        url_re = re.compile(r'https?://translate.google.com/translate_tts\.*')
        responses.add(responses.GET, url_re,
                      body='DATAMP3', status=200,
                      content_type='audio/mpeg')

        url = '/api/v1/core/tts/'
        message = "Lorem ipsum dolor sit amet, consectetur adipiscing elit." \
                  "Maecenas non justo tempor, ultrices nisi scelerisque," \
                  " blandit placerat nibh vulputate eget aenean laoreet " \
                  "ac mi nec rhoncus cras vel dui mauris nullam blandit " \
                  "urna eget dictum auctor aliquam sed suscipit felis, " \
                  "iaculis dapibus leo donec rutrum velit in ultricies " \
                  "accumsan tellus mauris vel facilisis dui ut congue " \
                  "lobortis lacus, suscipit vehicula ex mollis sit amet. " \
                  "Nam et justo ut est rhoncus congue at sed dui. Vivamus" \
                  " vitae urna volutpat, tempor odio sed, consequat orci." \
                  " Sed venenatis tincidunt tortor eget aliquam. " \
                  "Morbi efficitur venenatis elit," \
                  " blandit placerat nibh vulputate eget. Aenean laoreet " \
                  "ac mi nec rhoncus. Cras vel dui mauris. Nullam blandit " \
                  "urna eget dictum auctor. Aliquam sed suscipit felis, " \
                  "iaculis dapibus leo. Donec rutrum velit in ultricies " \
                  "pretium. Mauris id molestie lectus. Pellentesque fermentum."
        data = {'message': message, 'lang': 'en', 'driver': 'google'}
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

    def test_v1_tts_get_bad_driver(self):
        """
        Ensure we can send a message to tts
        """
        url = '/api/v1/core/tts/'
        data = {'message': u'bonjour', 'lang': 'en', 'driver': 'test'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_v1_tts_bad_request(self):
        """
        Ensure parameters are mandatory
        """
        url = '/api/v1/core/tts/'
        data = {}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @responses.activate
    def test_v1_tts_get_google_fail(self):
        """
        Ensure we can send a message to tts
        """
        url_re = re.compile(r'https?://translate.google.com/translate_tts\.*')
        responses.add(responses.GET, url_re,
                      body='DATAMP3', status=500,
                      content_type='audio/mpeg')

        url = '/api/v1/core/tts/'
        data = {'message': u'bonjour', 'lang': 'en', 'driver': 'google'}
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
