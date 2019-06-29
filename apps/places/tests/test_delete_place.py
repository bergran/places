# -*- coding: utf-8 -*-
from starlette import status

from apps.places.models import Place
from core.test.transaction_test_case import TransactionTestCase


class PlaceDeleteTestCase(TransactionTestCase):

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
        response = self.client.delete(self.get_url(self.place2.id + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_successfully(self):
        response = self.client.delete(self.get_url(self.place1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
