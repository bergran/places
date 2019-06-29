# -*- coding: utf-8 -*-

import factory

from apps.places.models import Place
from core.config import RESOURCE_ORIGIN_DUMMY_DATA
from core.db import common


class PlaceFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Place
        sqlalchemy_session = common.Session

    name = factory.Sequence(lambda n: u'place %d' % n)
    resource_origin = factory.Sequence(lambda n: RESOURCE_ORIGIN_DUMMY_DATA)
