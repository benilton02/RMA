from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.main.routes import (
    auth_router,
    index_router,
    rma_router
)

from core.infra.redis.redis_cli import redis_dependency

ORIGINS = ['*']

app = FastAPI()


@app.on_event('startup')
async def on_startup():
    await redis_dependency.init()


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

routers = (auth_router, index_router, rma_router)

[app.include_router(router) for router in routers]
