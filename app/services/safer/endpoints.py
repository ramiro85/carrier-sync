from fastapi import APIRouter

from app.core.schemas import ResponseModel
from app.services.safer.schemas import Company
from app.services.safer.controller import check_company

router = APIRouter()


@router.api_route(
    methods=["GET"],
    path="/api/safer/search/{query_field}/{query_value}",
    deprecated=False,
)
def search_company(query_field: str, query_value: str) -> Company | ResponseModel:
    """Look up a carrier profile by query field/value in the SAFER public database."""
    return check_company(query_field, query_value)
