# -*- coding: utf-8 -*-

from fastapi.routing import APIRouter
from apps.places.views import places


router = APIRouter()
router.include_router(places.router, prefix='/places')
