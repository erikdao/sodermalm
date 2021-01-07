import logging

from fastapi import FastAPI
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import Response

from sodermalm.api import api_router
from sodermalm.database import SessionLocal

logger = logging.getLogger(__name__)

# Create the starlette ASGI for the app
app = Starlette()


@app.middleware('http')
async def db_session_middleware(request: Request, call_next):
    response = Response('Internal Server Error', status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Create the API framework
api = FastAPI()
api.include_router(api_router, prefix='/v1')

app.mount('/api', app=api)
