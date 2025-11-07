from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Profile(Base):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(String(64), primary_key=True, index=True)
    nickname: Mapped[str | None] = mapped_column(String(100), nullable=True)
    homepage_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    public_contact: Mapped[bool] = mapped_column(Boolean, default=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    bio: Mapped[str | None] = mapped_column(String(1024), nullable=True)
    organization: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    social_links: Mapped[str | None] = mapped_column(String(1024), nullable=True)  # JSON string
