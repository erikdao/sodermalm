import logging

from fastapi import FastAPI
from starlette.applications import Starlette

from sodermalm.api import api_router

logger = logging.getLogger(__name__)

# Create the starlette ASGI for the app
app = Starlette()

# Create the API framework
api = FastAPI()
api.include_router(api_router, prefix='/v1')

app.mount('/api', app=api)
