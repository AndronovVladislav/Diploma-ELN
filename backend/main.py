from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import setup_db
from routes.auth import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0613
    await setup_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
