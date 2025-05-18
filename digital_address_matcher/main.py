"""Главный поток приложения."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from digital_address_matcher.routers import root_router, tags_meta


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan.
    """
    # действия выполняемые перед стартом

    yield

    # действия выполняемые перед остановкой


app = FastAPI(
    title='Digital Address Matcher',
    description='Digital Address Matcher',
    version='0.0.0',
    openapi_tags=tags_meta,
    lifespan=lifespan,
)


app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(root_router)



@app.get('/')
async def root(request: Request):
    """Корневой роутер."""
    return RedirectResponse('{}docs'.format(request.url))
