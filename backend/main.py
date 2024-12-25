from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import setup_db
from routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await setup_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(users_router)
