from fastapi.routing import APIRouter

from apps.health_check.views.health_check import router as routes

router = APIRouter()

router.include_router(routes)
