# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.places.models import Place
from apps.places.serializers.place import PlaceOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class PlaceRetrieveTestCase(TransactionTestCase):

    def setUp(self):
        self.place1 = Place(name='Stormwind City', resource_origin='testserver')
        self.place2 = Place(name='Orgrimmar', resource_origin='testserver')

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
        response = self.client.get(self.get_url(self.place2.id + 1))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_place_1(self):
        response = self.client.get(self.get_url(self.place1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload_dict = PlaceOutSerializer(**response.json()).dict()
        self.assertEqual(PlaceOutSerializer(**jsonable_encoder(self.place1)).dict(), payload_dict)

    def test_get_place_2(self):
        response = self.client.get(self.get_url(self.place2.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload_dict = PlaceOutSerializer(**response.json()).dict()
        self.assertEqual(PlaceOutSerializer(**jsonable_encoder(self.place2)).dict(), payload_dict)
