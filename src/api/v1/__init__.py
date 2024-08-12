from fastapi import APIRouter

from src.api.v1.students import router as students_router

routers = (
    students_router,
)

router_v1 = APIRouter(prefix="/v1")

for router in routers:
    router_v1.include_router(router)
