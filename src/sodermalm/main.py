import logging

from fastapi import FastAPI

logger = logging.getLogger(__name__)

app = FastAPI()


@app.get('/')
async def index():
    return {'key': 'value'}


@app.get('/healthcheck')
async def health_check():
    return {'status': 'OK'}
