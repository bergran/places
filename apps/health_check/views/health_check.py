# -*- coding: utf-8 -*-


from fastapi.routing import APIRouter

router = APIRouter()


@router.get("/health-check")
async def health_check():
    return {}
