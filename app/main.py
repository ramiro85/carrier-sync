import os

from fastapi import FastAPI, APIRouter

from app.core import core_endpoints

router = APIRouter()
__version__ = "1.0"
app = FastAPI(
    title="Integration Utility API",
    summary="API integration service for broker verification, debtor lookup, email, and ELD workflows.",
    version="1.0" + "-" + os.environ.get("commit_sha", "unknown")[:7],
    description=(
        "REST API that integrates external transportation services for "
        "carrier lookup, debtor data, Gmail workflows, and ELD driver operations."
    ),
)
app.include_router(core_endpoints.router)
