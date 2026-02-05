from fastapi import APIRouter

from app.routers.movies import movie_router

main_router = APIRouter()

main_router.include_router(movie_router)
