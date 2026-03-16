from typing import Optional, Any

from pydantic import BaseModel


class ResponseModel(BaseModel):
    success: bool
    message: str
    data: Optional[Any]
