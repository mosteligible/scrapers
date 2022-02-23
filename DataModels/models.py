from optparse import Option
from typing import Optional
from pydantic import BaseModel, EmailStr


class CrawlInitiator(BaseModel):
    url: str
    num_pages: int
    email: Optional[EmailStr] = None
    phone: Optional[int] = None
