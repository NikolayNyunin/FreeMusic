import sqlite3
from typing import Sequence

from sqlalchemy import create_engine, select, delete
from sqlalchemy.orm import Session
import bcrypt

from db import Base, User, Artist


class MusicSession:
    """Класс сессии работы с приложением."""

    def __init__(self) -> None:
        """Инициализация сессии."""

        self.engine = create_engine('sqlite:///music.db', echo=True)

        Base.metadata.create_all(self.engine)

        self.user = None

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

        # успешная попытка входа
        # сохранение данных о текущем пользователе
        self.user = user
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
            except sqlite3.IntegrityError:  # TODO: catch other exceptions
                session.rollback()
                return False, 'The user with this login already exists'
            else:
                return True, 'Success'

    def edit_account(self, password: str = None, username: str = None,
                     bio: str = None) -> (bool, str):
        """Редактирование данных аккаунта."""

        # попытка редактирования данных аккаунта
        with Session(self.engine) as session:
            try:
                user = session.query(User).get(self.user.id)
                if password is not None:
                    # хеширование пароля
                    password_hash_and_salt = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                    user.password_hash = password_hash_and_salt
                if username is not None:
                    user.username = username
                if bio is not None:
                    user.bio = bio
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                self.user = session.scalars(select(User).where(User.id == user.id)).one()
                return True, 'Success'

    def log_out(self) -> None:
        """Выход из аккаунта."""

        self.user = None

    def add_artist(self, name: str, description: str) -> (bool, str):
        """Добавление исполнителя."""

        # TODO: проверка полномочий

        # создание экземпляра класса исполнителя
        artist = Artist(
            name=name,
            description=description
        )

        # попытка добавления исполнителя
        with Session(self.engine) as session:
            try:
                session.add(artist)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Success'

    def get_all_artists(self) -> Sequence[Artist]:
        """Получение списка из всех исполнителей."""

        with Session(self.engine) as session:
            statement = select(Artist)
            artists = session.scalars(statement).all()

        return artists

    def delete_artist(self, artist_id: int) -> (bool, str):
        """Удаление исполнителя по ID."""

        # TODO: проверка полномочий

        # попытка удаления исполнителя
        with Session(self.engine) as session:
            statement = delete(Artist).where(Artist.id == artist_id)
            session.execute(statement)
            session.commit()

        return True, 'Success'
