from typing import Optional

from pydantic import BaseModel as PydanticBaseModel


class TafsUser(PydanticBaseModel):
    username: Optional[str] = None

    class Config:
        from_attributes = True


class TafDebtor(PydanticBaseModel):
    account_id: str | None = None
    mc_number: str | None = None
    debtor_name: str | None = None
    debtor_buy_status: str | None = None
    is_denied: bool | None = None
    debtor_rating: str | None = None
    debtor_credit_limit: str | None = None
    debtor_address: str | None = None
    debtor_msg: str | None = None
    tafs_html: str | None = None

    class Config:
        from_attributes = True
