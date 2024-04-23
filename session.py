import sqlite3
from typing import Sequence
from datetime import date

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import bcrypt

from db import Base, User, Album, Artist, Genre


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

    def add_album(self, name: str, release_date: date, artist_id: int) -> (bool, str):
        """Добавление альбома."""

        # TODO: проверка полномочий

        # создание экземпляра класса альбома
        album = Album(
            name=name,
            release_date=release_date,
            artist_id=artist_id
        )

        # попытка добавления исполнителя
        with Session(self.engine) as session:
            try:
                session.add(album)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Success'

    def get_all_albums(self) -> Sequence[Album]:
        """Получение списка из всех альбомов."""

        with Session(self.engine) as session:
            statement = select(Album)
            albums = session.scalars(statement).all()

        return albums

    def delete_album(self, album_id: int) -> (bool, str):
        """Удаление альбома по ID."""

        # TODO: проверка полномочий

        # попытка удаления альбома
        with Session(self.engine) as session:
            try:
                album = session.query(Album).filter(Album.id == album_id).first()
                session.delete(album)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Success'

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

    def get_artist(self, artist_id: int) -> Artist:
        """Получение исполнителя по ID."""

        with Session(self.engine) as session:
            statement = select(Artist).where(Artist.id == artist_id)
            artist = session.scalars(statement).one()

        return artist

    def delete_artist(self, artist_id: int) -> (bool, str):
        """Удаление исполнителя по ID."""

        # TODO: проверка полномочий

        # попытка удаления исполнителя
        with Session(self.engine) as session:
            try:
                artist = session.query(Artist).filter(Artist.id == artist_id).first()
                session.delete(artist)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Success'

    def add_genre(self, name: str) -> (bool, str):
        """Добавление жанра."""

        # TODO: проверка полномочий

        # создание экземпляра класса жанра
        genre = Genre(name=name)

        # попытка добавления жанра
        with Session(self.engine) as session:
            try:
                session.add(genre)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Success'

    def get_all_genres(self) -> Sequence[Genre]:
        """Получение списка из всех жанров."""

        with Session(self.engine) as session:
            statement = select(Genre)
            genres = session.scalars(statement).all()

        return genres

    def delete_genre(self, genre_id: int) -> (bool, str):
        """Удаление жанра по ID."""

        # TODO: проверка полномочий

        # попытка удаления жанра
        with Session(self.engine) as session:
            try:
                genre = session.query(Genre).filter(Genre.id == genre_id).first()
                session.delete(genre)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Success'
