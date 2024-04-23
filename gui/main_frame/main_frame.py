from tkinter import ttk

from gui.main_frame.album_frame import AlbumFrame
from gui.main_frame.artist_frame import ArtistFrame
from gui.main_frame.genre_frame import GenreFrame
from gui.main_frame.account_frame import AccountFrame


class MainFrame(ttk.Frame):
    """Основной виджет приложения."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        padding = {'padx': 10, 'pady': 10}

        self.app = container

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.columnconfigure(4, weight=4)
        self.columnconfigure(5, weight=1)

        self.tracks_button = ttk.Button(self, text='Композиции', command=self.show_tracks)
        self.tracks_button.grid(row=0, column=0, **padding)

        self.albums_button = ttk.Button(self, text='Альбомы', command=self.show_albums)
        self.albums_button.grid(row=0, column=1, **padding)

        self.artists_button = ttk.Button(self, text='Исполнители', command=self.show_artists)
        self.artists_button.grid(row=0, column=2, **padding)

        self.genres_button = ttk.Button(self, text='Жанры', command=self.show_genres)
        self.genres_button.grid(row=0, column=3, **padding)

        self.account_button = ttk.Button(self, text='Аккаунт', command=self.show_account)
        self.account_button.grid(row=0, column=4, sticky='e', **padding)

        self.menu_buttons = [self.tracks_button, self.albums_button, self.artists_button,
                             self.genres_button, self.account_button]

        self.log_out_button = ttk.Button(self, text='Выйти', command=self.log_out)
        self.log_out_button.grid(row=0, column=5, sticky='w', **padding)

        self.album_frame = AlbumFrame(self)
        self.album_frame.grid(row=1, column=0, columnspan=6, sticky='nsew', **padding)

        self.artist_frame = ArtistFrame(self)
        self.artist_frame.grid(row=1, column=0, columnspan=6, sticky='nsew', **padding)

        self.genre_frame = GenreFrame(self)
        self.genre_frame.grid(row=1, column=0, columnspan=6, sticky='nsew', **padding)

        self.account_frame = AccountFrame(self)
        self.account_frame.grid(row=1, column=0, columnspan=6, sticky='nsew', **padding)

    def enable_menu_buttons(self) -> None:
        """Активация всех кнопок меню."""

        for button in self.menu_buttons:
            button.configure(state='normal')

    def reset(self) -> None:
        """Сброс состояния виджета."""

        self.show_tracks()

    def show_tracks(self) -> None:
        """Отображение списка композиций."""

        # TODO: implement

    def show_albums(self) -> None:
        """Отображение списка альбомов."""

        # включение всех кнопок меню
        self.enable_menu_buttons()

        # выключение нажатой кнопки
        self.albums_button.configure(state='disabled')

        # обновление и отображение виджета списка альбомов
        self.album_frame.update()
        self.album_frame.tkraise()

    def show_artists(self) -> None:
        """Отображение списка исполнителей."""

        # включение всех кнопок меню
        self.enable_menu_buttons()

        # выключение нажатой кнопки
        self.artists_button.configure(state='disabled')

        # обновление и отображение виджета списка исполнителей
        self.artist_frame.update()
        self.artist_frame.tkraise()

    def show_genres(self) -> None:
        """Отображение списка жанров."""

        # включение всех кнопок меню
        self.enable_menu_buttons()

        # выключение нажатой кнопки
        self.genres_button.configure(state='disabled')

        # обновление и отображение виджета списка жанров
        self.genre_frame.update()
        self.genre_frame.tkraise()

    def show_account(self) -> None:
        """Отображение настроек аккаунта."""

        # включение всех кнопок меню
        self.enable_menu_buttons()

        # выключение нажатой кнопки
        self.account_button.configure(state='disabled')

        # сброс и отображение виджета редактирования аккаунта
        self.account_frame.reset()
        self.account_frame.tkraise()

    def log_out(self) -> None:
        """Выход из аккаунта."""

        self.app.session.log_out()
        self.app.show_login_frame()
