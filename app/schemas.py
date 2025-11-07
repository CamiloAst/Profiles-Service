from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

class ProfileIn(BaseModel):
    nickname: Optional[str] = None
    homepage_url: Optional[str] = None
    public_contact: Optional[bool] = False
    address: Optional[str] = None
    bio: Optional[str] = None
    organization: Optional[str] = None
    country: Optional[str] = None
    social_links: Optional[Dict[str, Any]] = None

class ProfileOut(ProfileIn):
    user_id: str
