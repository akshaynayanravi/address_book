from pydantic import BaseModel

from typing import Optional


class AddressBase(BaseModel):
    name: str
    description: Optional[str]
    lattitude: float
    longitude: float
    