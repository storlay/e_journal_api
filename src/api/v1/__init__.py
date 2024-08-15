from fastapi import APIRouter

from src.api.v1.scores import router as scores_router
from src.api.v1.students import router as students_router
from src.config.config import settings

routers = (
    scores_router,
    students_router,
)

router_v1 = APIRouter(prefix=settings.api.V1_PREFIX)

for router in routers:
    router_v1.include_router(router)
