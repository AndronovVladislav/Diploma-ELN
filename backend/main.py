from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import setup_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield


app = FastAPI(lifespan=lifespan)
# app = FastAPI()
