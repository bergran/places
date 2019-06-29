# -*- coding: utf-8 -*-
from typing import List

from fastapi import Depends, HTTPException, Query
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import Response, UJSONResponse

from apps.places.models import Place
from apps.places.serializers.place import PlaceSerializer, PlaceOutSerializer
from apps.places.service.send_delete import send_delete_place
from apps.places.utils.check_if_exists_place import check_if_exists
from core import config
from core.depends import get_database
from core.utils.get_object_or_404 import get_object_or_404

router = APIRouter()


@router.get('/', response_model=List[PlaceOutSerializer])
def list_places(session: Session = Depends(get_database), page: int = Query(1, regex = r'[1-9]+')):
    page_size = config.PAGE_SIZE
    page -= 1
    return session.query(Place).filter(Place.deleted_.is_(False)).limit(page_size).offset(page*page_size).all()


@router.get('/{place_id}', response_model=PlaceOutSerializer)
def read_places(place_id: int, session: Session = Depends(get_database)):
    obj = get_object_or_404(session.query(Place).filter(Place.deleted_.is_(False), Place.id == place_id))
    return obj


@router.post('/', response_model=PlaceOutSerializer, status_code=status.HTTP_201_CREATED)
async def create_place(
        place: PlaceSerializer,
        session: Session = Depends(get_database),
):
    if check_if_exists(place, session):
        raise HTTPException(detail='this name place exists', status_code=status.HTTP_400_BAD_REQUEST)

    place_obj = Place(**place.dict())
    session.add(place_obj)
    session.commit()
    session.refresh(place_obj)
    return place_obj


@router.put('/{place_id}', response_model=PlaceOutSerializer)
def update_place(place_id: int, place: PlaceSerializer, session: Session = Depends(get_database)):
    obj = get_object_or_404(session.query(Place).filter(Place.deleted_.is_(False), Place.id == place_id))
    if check_if_exists(place, session):
        raise HTTPException(detail='this name place exists', status_code=status.HTTP_400_BAD_REQUEST)

    obj.name = place.name
    obj.resource_origin = place.resource_origin
    session.commit()
    return obj


@router.delete('/{place_id}')
async def delete_place(
        place_id: int,
        session: Session = Depends(get_database),
):
    obj = get_object_or_404(session.query(Place).filter(Place.deleted_.is_(False), Place.id == place_id))

    await perform_delete(obj, session)
    return UJSONResponse(status_code=status.HTTP_204_NO_CONTENT)


async def perform_delete(obj, session):
    response = await send_delete_place(obj)

    can_delete_ = False

    if response and response.status == status.HTTP_200_OK:
        can_delete_ = True

    if can_delete_:
        obj.deleted_ = True
        session.commit()
        session.refresh(obj)


# TODO - make a debug hook
if config.DEBUG:
    @router.delete('/{id}/hook-delete')
    def hook_delete_place():
        return Response(status_code=status.HTTP_200_OK)
