from datetime import datetime, date
from typing import List

from sqlalchemy import func, Column, String, ForeignKey, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# вспомогательная таблица для создания отношения many-to-many
track_to_genre = Table(
    'track_to_genre',
    Base.metadata,
    Column('track_id', ForeignKey('track.id'), primary_key=True),
    Column('genre_id', ForeignKey('genre.id'), primary_key=True)
)


class User(Base):
    """Пользователь приложения."""

    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(60))
    username: Mapped[str] = mapped_column(String(50))
    bio: Mapped[str] = mapped_column(String(1000), nullable=True)
    is_admin: Mapped[bool] = mapped_column(insert_default=False)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    def __repr__(self):
        return f'<User {self.username} ({self.login})>'


class Track(Base):
    """Композиция."""

    __tablename__ = 'track'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    audio_id: Mapped[str] = mapped_column(String(24), nullable=True)
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    album_id: Mapped[int] = mapped_column(ForeignKey('album.id'))
    album: Mapped['Album'] = relationship(back_populates='tracks')

    genres: Mapped[List['Genre']] = relationship(
        secondary=track_to_genre, back_populates='tracks'
    )

    def __repr__(self):
        return f'<Track {self.name} from {self.album}>'


class Album(Base):
    """Альбом."""

    __tablename__ = 'album'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    release_date: Mapped[date] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    artist_id: Mapped[int] = mapped_column(ForeignKey('artist.id'))
    artist: Mapped['Artist'] = relationship(back_populates='albums')

    tracks: Mapped[List['Track']] = relationship(back_populates='album', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Album {self.name} by {self.artist}>'


class Artist(Base):
    """Исполнитель."""

    __tablename__ = 'artist'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    albums: Mapped[List['Album']] = relationship(back_populates='artist', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Artist {self.name}>'


class Genre(Base):
    """Жанр."""

    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())

    tracks: Mapped[List['Track']] = relationship(
        secondary=track_to_genre, back_populates='genres'
    )

    def __repr__(self):
        return f'<Genre {self.name}>'
