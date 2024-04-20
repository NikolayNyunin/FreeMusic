from tkinter import ttk


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

        self.log_out_button = ttk.Button(self, text='Выйти', command=self.log_out)
        self.log_out_button.grid(row=0, column=5, sticky='w', **padding)

    def reset(self) -> None:
        """Сброс состояния виджета."""

        self.show_tracks()

    def show_tracks(self) -> None:
        """Отображение списка композиций."""

        # TODO: implement

    def show_albums(self) -> None:
        """Отображение списка альбомов."""

        # TODO: implement

    def show_artists(self) -> None:
        """Отображение списка исполнителей."""

        # TODO: implement

    def show_genres(self) -> None:
        """Отображение списка жанров."""

        # TODO: implement

    def show_account(self) -> None:
        """Отображение настроек аккаунта."""

        # TODO: implement

    def log_out(self) -> None:
        """Выход из аккаунта."""

        self.app.session.log_out()
        self.app.show_login_frame()
