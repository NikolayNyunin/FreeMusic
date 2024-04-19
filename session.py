import sqlite3

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

        # запрос пользователя по логину
        with Session(self.engine) as session:
            statement = select(User).where(User.login == login)
            users = session.scalars(statement).all()

        # если пользователь с данным логином не найден
        if len(users) == 0:
            return False, 'Wrong login'

        user = users[0]

        # проверка совпадения пароля
        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return False, 'Wrong password'

        return True, 'Success'

    def sign_up(self, login: str, password: str, username: str, bio: str) -> (bool, str):
        """Создание нового аккаунта."""

        # хеширование пароля
        password_hash_and_salt = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # создание экземпляра класса пользователя
        user = User(
            login=login,
            password_hash=password_hash_and_salt,
            username=username,
            bio=bio
        )

        # попытка добавления пользователя в БД
        with Session(self.engine) as session:
            try:
                session.add(user)
                session.commit()
            except sqlite3.IntegrityError:
                session.rollback()
                return False, 'The user with this login already exists'
            else:
                return True, 'Success'
