# -*- coding: utf-8 -*-
from datetime import datetime

from pydantic import BaseModel


class PlaceSerializer(BaseModel):
    name: str
    resource_origin: str

    class Config:
        orm_mode = True


class PlaceOutSerializer(PlaceSerializer):
    id: int
    created: datetime = None

