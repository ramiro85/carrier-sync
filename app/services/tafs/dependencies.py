from fastapi import HTTPException, status
from app.core.controllers import ctrl  # Your global controller registry


async def get_active_tafs_session():
    """
    Dependency that ensures the scraper is ready.
    Injects the controller only if authenticated.
    """
    tafs = ctrl.tafs_ctrl  # Access the singleton/instance

    if not tafs.is_authenticated():
        if not tafs.login():
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="TAFS Portal authentication failed.",
            )
    return tafs
