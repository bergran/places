# -*- coding: utf-8 -*-

from starlette import status

from core.test.transaction_test_case import TransactionTestCase


class PlaceCreateTestCase(TransactionTestCase):

    def get_url(self):
        return '/api/v1/places/'

    def test_create_succesfully(self):
        place = {
            'name': 'Orgrimmar',
            'resource_origin': 'testserver'
        }

        response = self.client.post(self.get_url(), json=place)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(place.get('name'), response.json().get('name'))

    def test_create_fails_validation(self):
        place = {
            'name': 'Orgrimmar',
            'resource_origin': 'testserver'
        }

        response = self.client.post(self.get_url(), json=place)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(place.get('name'), response.json().get('name'))

        response = self.client.post(self.get_url(), json=place)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
