import sqlite3
from typing import Sequence
from datetime import date

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import bcrypt
from pymongo import MongoClient
from bson.objectid import ObjectId
from gridfs import GridFS, GridOut

from db import Base, User, Track, Album, Artist, Genre


class MusicSession:
    """Класс сессии работы с приложением."""

    def __init__(self) -> None:
        """Инициализация сессии."""

        self.engine = create_engine('sqlite:///music.db', echo=True)

        Base.metadata.create_all(self.engine)

        mongo_client = MongoClient()
        mongo_db = mongo_client['music_db']
        self.grid_fs = GridFS(mongo_db)

        self.user = None

    def login(self, login: str, password: str) -> (bool, str):
        """Вход в аккаунт."""

        # запрос пользователя по логину
        with Session(self.engine) as session:
            statement = select(User).where(User.login == login)
            users = session.scalars(statement).all()

        # если пользователь с данным логином не найден
        if len(users) == 0:
            return False, 'Неверный логин'

        user = users[0]

        # проверка совпадения пароля
        if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return False, 'Неверный пароль'

        # успешная попытка входа
        # сохранение данных о текущем пользователе
        self.user = user
        return True, 'Успех'

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
                return False, 'Пользователь с данным логином уже существует'
            else:
                return True, 'Успех'

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
                return True, 'Успех'

    def log_out(self) -> None:
        """Выход из аккаунта."""

        self.user = None

    def add_track(self, name: str, audio_file_path: str, album_id: int, genre_ids: tuple[int]) -> (bool, str):
        """Добавление композиции."""

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

        # сохранение аудиофайла в MongoDB GridFS
        audio_id = self.save_audio_file(audio_file_path)

        # создание экземпляра класса композиции
        track = Track(
            name=name,
            audio_id=audio_id,
            album_id=album_id
        )

        for genre_id in genre_ids:
            track.genres.append(self.get_genre(genre_id))

        # попытка добавления композиции
        with Session(self.engine) as session:
            try:
                session.add(track)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Успех'

    def save_audio_file(self, audio_file_path: str) -> str:
        """Сохранение аудиофайла и возвращение его _id в MongoDB."""

        filename = audio_file_path.split('/')[-1]

        with open(audio_file_path, 'rb') as audio_file:
            audio_file_id = self.grid_fs.put(audio_file, filename=filename)

        return str(audio_file_id)

    def get_audio_file(self, audio_file_id: str) -> GridOut:
        """Получение аудиофайла по его _id в MongoDB."""

        return self.grid_fs.get(ObjectId(audio_file_id))

    def get_all_tracks(self) -> Sequence[Track]:
        """Получение списка из всех композиций."""

        with Session(self.engine) as session:
            statement = select(Track)
            tracks = session.scalars(statement).all()

        return tracks

    def delete_track(self, track_id: int) -> (bool, str):
        """Удаление композиции по ID."""

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

        # попытка удаления композиции
        with Session(self.engine) as session:
            try:
                track = session.query(Track).filter(Track.id == track_id).first()
                self.grid_fs.delete(track.audio_id)  # удаление аудиофайла из MongoDB
                session.delete(track)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Успех'

    def add_album(self, name: str, release_date: date, artist_id: int) -> (bool, str):
        """Добавление альбома."""

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

        # создание экземпляра класса альбома
        album = Album(
            name=name,
            release_date=release_date,
            artist_id=artist_id
        )

        # попытка добавления альбома
        with Session(self.engine) as session:
            try:
                session.add(album)
                session.commit()
            except Exception as e:
                session.rollback()
                return False, e
            else:
                return True, 'Успех'

    def get_all_albums(self) -> Sequence[Album]:
        """Получение списка из всех альбомов."""

        with Session(self.engine) as session:
            statement = select(Album)
            albums = session.scalars(statement).all()

        return albums

    def get_albums(self, artist_id: int) -> Sequence[Album]:
        """Получение списка из альбомов исполнителя по его ID."""

        with Session(self.engine) as session:
            statement = select(Artist).where(Artist.id == artist_id)
            albums = session.scalars(statement).one().albums

        return albums

    def get_album(self, album_id: int) -> Album:
        """Получение альбома по ID."""

        with Session(self.engine) as session:
            statement = select(Album).where(Album.id == album_id)
            album = session.scalars(statement).one()

        return album

    def delete_album(self, album_id: int) -> (bool, str):
        """Удаление альбома по ID."""

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

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
                return True, 'Успех'

    def add_artist(self, name: str, description: str) -> (bool, str):
        """Добавление исполнителя."""

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

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
                return True, 'Успех'

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

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

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
                return True, 'Успех'

    def add_genre(self, name: str) -> (bool, str):
        """Добавление жанра."""

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

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
                return True, 'Успех'

    def get_all_genres(self) -> Sequence[Genre]:
        """Получение списка из всех жанров."""

        with Session(self.engine) as session:
            statement = select(Genre)
            genres = session.scalars(statement).all()

        return genres

    def get_genres(self, track_id: int) -> Sequence[Genre]:
        """Получение списка из жанров композиции по её ID."""

        with Session(self.engine) as session:
            statement = select(Track).where(Track.id == track_id)
            genres = session.scalars(statement).one().genres

        return genres

    def get_genre(self, genre_id: int) -> Genre:
        """Получение жанра по ID."""

        with Session(self.engine) as session:
            statement = select(Genre).where(Genre.id == genre_id)
            genre = session.scalars(statement).one()

        return genre

    def delete_genre(self, genre_id: int) -> (bool, str):
        """Удаление жанра по ID."""

        if self.user is None or not self.user.is_admin:
            return False, 'Отказано в доступе'

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
                return True, 'Успех'
