from pydantic import BaseModel


class Address(BaseModel):
    address: str | None = None
    city: str | None = None
    state: str | None = None
    zip: str | None = None
    full_address: str | None = None


class Company(BaseModel):
    founded: bool
    entity_type: str | None = None
    mc_number: str | None = None
    usdot_number: str | None = None
    usdot_status: str | None = None
    legal_name: str | None = None
    dba_name: str | None = None
    phone: str | None = None
    message: str | None = None
    operating_authority_status: str | None = None
    physical_address: Address | None = None
    mailing_address: Address | None = None

    class Config:
        from_attributes = True
