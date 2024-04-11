from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import bcrypt

from db import Base, User


class MusicSession:
    """Класс сессии работы с приложением."""

    def __init__(self) -> None:
        """Инициализация сессии."""

        self.engine = create_engine('sqlite:///music.db', echo=True)

        Base.metadata.create_all(self.engine)

    def login(self, login: str, password: str) -> (bool, str):
        """Вход в аккаунт."""

        with Session(self.engine) as session:
            statement = select(User).where(User.login == login)
            users = session.scalars(statement).all()

        if len(users) == 0:
            return False, 'Wrong login'

        user = users[0]
        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return False, 'Wrong password'

        return True, 'Success'
