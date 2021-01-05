from typing import Optional

from fastapi import APIRouter

from .models import Team

router = APIRouter()


@router.get('/')
async def get_teams():
    teams = [
        Team(id=1, name='Test team')
    ]
    return teams


@router.post('/')
async def create_team(team: Team, q: Optional[str] = None):
    return team
