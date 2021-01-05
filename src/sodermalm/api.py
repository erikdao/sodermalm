from fastapi import APIRouter

from sodermalm.team.views import router as team_router

api_router = APIRouter()

api_router.include_router(team_router, prefix='/teams', tags=['teams'])
