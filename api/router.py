from fastapi import APIRouter

from api.routers import auth, projects, users


api_router = APIRouter(prefix="/v0")

api_router.include_router(
    router=auth.router,
    prefix="/auth",
    tags=["Auth"],
)

api_router.include_router(
    router=users.router,
    prefix="/users",
    tags=["Users"],
)

api_router.include_router(
    router=projects.router,
    prefix="/projects",
    tags=["Projects"],
)
