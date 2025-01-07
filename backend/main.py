from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from auth.auth import router as auth_router
from db.utils import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0621,W0613
    await db_helper.setup()
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)


if __name__ == '__main__':
    uvicorn.run(app)
