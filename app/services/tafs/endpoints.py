from fastapi import APIRouter, Depends

from app.services.tafs.controller import TafsController
from app.services.tafs.dependencies import get_active_tafs_session

router = APIRouter()


@router.get("/api/tafs/search_broker/{mc}")
def search_broker(
    mc: str,
    tafs: TafsController = Depends(get_active_tafs_session),
) -> dict:
    """Search broker information and associated debtor data by MC number."""
    response = tafs.search_broker(mc)
    return {"brokers": response}


@router.get("/api/tafs/load_debtor/{account_id}")
def load_debtor(
    account_id: str,
    mc: str | None = None,
    tafs: TafsController = Depends(get_active_tafs_session),
) -> dict:
    """Load full debtor details for an account ID."""
    _ = mc  # Kept for backward compatibility with existing query callers.
    response = tafs.load_debtor(account_id)
    return {"debtor": response}
