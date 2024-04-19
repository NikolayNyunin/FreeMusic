from datetime import datetime

from sqlalchemy import func, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(63))
    username: Mapped[str] = mapped_column(String(50))
    bio: Mapped[str] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self):
        return f'<User {self.username} ({self.login})>'
