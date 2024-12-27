from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from auth.auth import router as auth_router
from db import setup_db


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0621,W0613
    await setup_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run(app)
