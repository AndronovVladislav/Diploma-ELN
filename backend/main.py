from contextlib import asynccontextmanager

from fastapi import FastAPI

from models import setup_db
from routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0613
    await setup_db()
    yield


main_app = FastAPI(lifespan=lifespan)
main_app.include_router(users_router)
