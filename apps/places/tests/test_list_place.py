# -*- coding: utf-8 -*-
from fastapi.encoders import jsonable_encoder
from starlette import status

from apps.places.models import Place
from apps.places.serializers.place import PlaceOutSerializer
from core.test.transaction_test_case import TransactionTestCase


class PlaceListTestCase(TransactionTestCase):

    def setUp(self):
        self.place1 = Place(name='Stormwind City', resource_origin='testserver')
        self.place2 = Place(name='Orgrimmar', resource_origin='testserver')
        self.place3 = Place(name='Undercity', deleted_=True, resource_origin='testserver')

        self.create_models()

    def create_models(self):
        self.places = [self.place1, self.place2, self.place3]
        self.session.add_all(self.places)
        self.session.commit()

        self.refresh_models()

    def refresh_models(self):
        self.session.refresh(self.place1)
        self.session.refresh(self.place2)
        self.session.refresh(self.place3)

    def test_get_response(self):
        response = self.client.get('/api/v1/places')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = [PlaceOutSerializer(**place) for place in response.json()]

        self.assertEqual(len(self.places) - 1, len(payload))

        for place in self.places:
            if not place.deleted_:
                self.assertIn(PlaceOutSerializer(**jsonable_encoder(place)), payload)
