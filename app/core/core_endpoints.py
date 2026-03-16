from fastapi import APIRouter

from app.core.schemas import ResponseModel
from app.services.safer import endpoints as safer_endpoints
from app.services.tafs import endpoints as tafs_endpoints
from app.services.googleCloud import endpoints as google_endpoints
from app.services.eld.driver import endpoints as eld_endpoints

router = APIRouter()


@router.api_route("/health", methods=["POST"])
def health() -> ResponseModel:
    """Health endpoint used by probes and external monitors."""
    return ResponseModel(success=True, message="ok", data={"status": "healthy"})


# Google
router.include_router(google_endpoints.router, tags=["Google"])
# TAFS
router.include_router(tafs_endpoints.router, tags=["TAFS"])
# SAFER
router.include_router(safer_endpoints.router, tags=["SAFER"])
router.include_router(eld_endpoints.router, tags=["ELD"])
