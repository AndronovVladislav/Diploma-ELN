from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.models.utils import db_helper
from backend.routes.auth.auth import router as auth_router
from backend.routes.experiments.experiments import router as experiments_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=W0621,W0613
    yield
    await db_helper.dispose()


app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(experiments_router)

if settings.uvicorn.debug:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if __name__ == '__main__':
    uvicorn.run(app,
                host=settings.uvicorn.host,
                port=settings.uvicorn.port,
                workers=settings.uvicorn.workers,
                timeout_keep_alive=settings.uvicorn.timeout,
                )
