# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, UniqueConstraint, Boolean, Text, DateTime
from sqlalchemy.sql.functions import now

from core.db.base import Base


class Place(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(32), index=True)
    deleted_ = Column(Boolean, default=False)
    created = Column(DateTime, default=now())
    resource_origin = Column(Text)

    __table_args__ = (UniqueConstraint('name', name='unique_constrain_place_name'), )
