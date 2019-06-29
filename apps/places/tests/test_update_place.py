# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.places.models import Place
from apps.places.serializers.place import PlaceOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class PlaceUpdateTestCase(TransactionTestCase):

    def setUp(self):
        self.place1 = Place(name='Stormwind City')
        self.place2 = Place(name='Orgrimmar')

        self.create_models()
        self.refresh_models()

    def create_models(self):
        self.places = [self.place1, self.place2]
        self.session.add_all(self.places)
        self.session.commit()

    def refresh_models(self):
        self.session.refresh(self.place1)
        self.session.refresh(self.place2)

    def get_url(self, pk):
        return '/api/v1/places/{}'.format(pk)

    def test_no_response(self):
        updated_name = '{} updated'.format(self.place2.name)
        place = {
            'name': updated_name,
            'resource_origin': 'testserver'
        }

        response = self.client.put(self.get_url(self.place2.id + 1), json=place)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_successfully(self):
        updated_name = '{} updated'.format(self.place1.name)
        place = {
            'name': updated_name,
            'resource_origin': 'testserver'
        }
        response = self.client.put(self.get_url(self.place1.id), json=place)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(updated_name, response.json().get('name'))

    def test_update_error(self):
        updated_name = self.place2.name
        place = {
            'name': updated_name,
            'resource_origin': 'testserver'
        }

        response = self.client.put(self.get_url(self.place1.id), json=place)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
