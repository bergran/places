# -*- coding: utf-8 -*-

import aiohttp

from apps.places.models import Place
from core import config


async def send_delete_place(place: Place):
    hook_notify_client = config.HOOK_NOTIFY_CLIENT.format(place.id)

    if place.resource_origin and hook_notify_client:
        async with aiohttp.ClientSession() as session_service:
            async with session_service.delete('{}{}'.format(place.resource_origin, hook_notify_client)) as response:
                return response
    else:
        return None
