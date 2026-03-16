import os

from fastapi import FastAPI, APIRouter

from app.core import core_endpoints

router = APIRouter()
__version__ = "1.0"
app = FastAPI(
    title="Jobee API",
    summary="Application to use third part service like TAFS, Safer, Reliable",
    version="1.0" + "-" + os.environ.get("commit_sha", "unknown")[:7],
    description="""An API to use third part service like TAFS, Safer, ELD""", )
app.include_router(core_endpoints.router)


