from fastapi import APIRouter

from app.api.endpoints import room

api_router = APIRouter()

api_router.include_router(room.router, tags=["session"])
