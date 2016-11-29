import pytest
import requests

from django.test import TestCase


class TestSite(TestCase):
    @staticmethod
    def test_unknown_url():
        response = requests.get('http://127.0.0.1:8000/unknown')

        assert response.status_code == 404

    @staticmethod
    def test_known_url():
        response = requests.get('http://127.0.0.1:8000')

        assert response.status_code == 200

    # @staticmethod
    # def test_twitter_redirect():
    #     response = requests.get('http://127.0.0.1:8000/login/twitter/?next=/')
    #
    #     assert response.status_code == 200
