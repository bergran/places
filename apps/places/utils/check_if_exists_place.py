# -*- coding: utf-8 -*-
from apps.places.models import Place


def check_if_exists(place, session):
    exists = session.query(Place).filter(Place.name == place.name).first() is not None
    return exists
