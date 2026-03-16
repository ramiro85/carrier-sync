from fastapi import APIRouter, Depends

from app.services.tafs.controller import TafsController
from app.services.tafs.dependencies import get_active_tafs_session

router = APIRouter()

@router.get("/api/tafs/search_broker/{mc}")
def search_broker(
    mc: str,
    tafs: TafsController = Depends(get_active_tafs_session)
):
    # 'tafs' here is the authenticated controller
    response = tafs.search_broker(mc)
    return {"brokers": response}

@router.get("/api/tafs/load_debtor/{account_id}")
def load_debtor(
    account_id: str,
    mc: str,
    tafs: TafsController = Depends(get_active_tafs_session)
):
    # This logic will only execute if the session is alive
    response = tafs.load_debtor(mc, account_id)
    return {"debtor": response}