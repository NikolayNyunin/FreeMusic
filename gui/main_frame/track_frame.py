import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import askokcancel, showinfo, showerror


class TrackFrame(ttk.Frame):
    """Виджет отображения и редактирования списка композиций."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        self.padding = {'padx': 10, 'pady': 10}

        self.session = container.app.session

        self.add_track_button = None

    def update(self) -> None:
        """Обновление состояния виджета."""

        # удаление всех дочерних виджетов
        for child in self.winfo_children():
            child.destroy()

        # если пользователь администратор
        # создание кнопки добавления композиции
        if self.session.user is not None:
            if self.session.user.is_admin:
                self.add_track_button = ttk.Button(self, text='Добавить композицию',
                                                   command=self.show_add_track_window)
                self.add_track_button.pack(side='top', **self.padding)

        # отображение списка композиций
        for track in self.session.get_all_tracks():
            track_frame = ttk.Frame(self)

            name_label = ttk.Label(track_frame, text=track.name)
            name_label.grid(row=0, column=0)

            album = self.session.get_album(track.album_id)

            artist_name_label = ttk.Label(track_frame, text=self.session.get_artist(album.artist_id).name)
            artist_name_label.grid(row=0, column=1)

            album_name_label = ttk.Label(track_frame, text=album.name)
            album_name_label.grid(row=0, column=2)

            # TODO: add audio

            genres_text = '\n'.join([g.name for g in self.session.get_genres(track.id)])
            genres_label = ttk.Label(track_frame, text=genres_text)
            genres_label.grid(row=0, column=3)

            if self.session.user is not None:
                if self.session.user.is_admin:
                    delete_button = ttk.Button(track_frame, text='Удалить',
                                               command=lambda track_id=track.id: self.delete_track(track_id))
                    delete_button.grid(row=0, column=4, **self.padding)

            track_frame.pack(side='top', **self.padding)

    def show_add_track_window(self) -> None:
        """Отображение окна добавления композиции."""

        add_track_window = AddTrackWindow(self)
        add_track_window.grab_set()

    def delete_track(self, track_id: int) -> None:
        """Удаление композиции."""

        # подтверждение удаления композиции
        confirmation = askokcancel(
            title='Подтверждение удаления композиции',
            message='Вы уверены, что хотите безвозвратно удалить композицию?',
            icon='warning'
        )
        if not confirmation:
            return

        # попытка удаления композиции
        success, message = self.session.delete_track(track_id)
        if success:
            self.update()
            showinfo(title='Успех', message='Удаление композиции прошло успешно')
        else:
            showerror(title='Ошибка удаления композиции', message=message)


class AddTrackWindow(tk.Toplevel):
    """Окно добавления композиции."""

    def __init__(self, parent):
        """Инициализация окна."""

        super().__init__(parent)

        padding = {'padx': 10, 'pady': 10}

        self.parent = parent

        self.geometry('540x360')
        self.title('Добавление альбома')

        self.rowconfigure(0, weight=2)
        self.rowconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=2)
        self.rowconfigure(4, weight=2)
        self.rowconfigure(5, weight=5)
        self.rowconfigure(6, weight=2)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.track_name_label = ttk.Label(self, text='Название композиции:')
        self.track_name_label.grid(row=0, column=0, **padding)

        self.track_name = tk.StringVar()
        self.track_name_entry = ttk.Entry(self, textvariable=self.track_name)
        self.track_name_entry.grid(row=0, column=1, **padding)

        self.audio_input_label = ttk.Label(self, text='Аудиофайл:')
        self.audio_input_label.grid(row=1, column=0, **padding)

        self.select_audio_file_button = ttk.Button(self, text='Выбрать файл', command=self.select_audio_file)
        self.select_audio_file_button.grid(row=1, column=1, **padding)

        self.filename = tk.StringVar()
        self.filename_label = ttk.Label(self, textvariable=self.filename)
        self.filename_label.grid(row=2, column=0, columnspan=2, **padding)

        self.artist_name_label = ttk.Label(self, text='Исполнитель:')
        self.artist_name_label.grid(row=3, column=0, **padding)

        # подготовка списка исполнителей для отображения
        artists = self.parent.session.get_all_artists()
        artist_names = tuple([a.name for a in artists])
        self.artist_ids = tuple([a.id for a in artists])

        self.artist_name = tk.StringVar()
        self.artist_name_combobox = ttk.Combobox(self, textvariable=self.artist_name,
                                                 values=artist_names, )
        self.artist_name_combobox.bind('<<ComboboxSelected>>', self.update_albums)
        self.artist_name_combobox.grid(row=3, column=1, **padding)

        self.album_name_label = ttk.Label(self, text='Альбом:')
        self.album_name_label.grid(row=4, column=0, **padding)

        # подготовка списка альбомов для отображения
        current_artist = self.artist_name_combobox.current()
        if current_artist == -1:
            albums = []
        else:
            albums = self.parent.session.get_albums(self.artist_ids[self.artist_name_combobox.current()])
        album_names = tuple([a.name for a in albums])
        self.album_ids = tuple([a.id for a in albums])

        self.album_name = tk.StringVar()
        self.album_name_combobox = ttk.Combobox(self, textvariable=self.album_name,
                                                values=album_names)
        self.album_name_combobox.grid(row=4, column=1, **padding)

        self.genres = self.parent.session.get_all_genres()
        if len(self.genres) != 0:
            self.genres_label = ttk.Label(self, text='Жанры:')
            self.genres_label.grid(row=5, column=0, **padding)

            self.genres_frame = ttk.Frame(self)

            self.selected_genres = [tk.BooleanVar() for _ in self.genres]
            for i, genre in enumerate(self.genres):
                genre_checkbutton = ttk.Checkbutton(self.genres_frame, text=genre.name,
                                                    variable=self.selected_genres[i])
                genre_checkbutton.pack(side='top')

            self.genres_frame.grid(row=5, column=1, **padding)

        self.add_track_button = ttk.Button(self, text='Добавить композицию', command=self.add_track)
        self.add_track_button.grid(row=6, column=0, columnspan=2, **padding)

    def select_audio_file(self):
        """Выбор аудиофайла композиции."""

        filename = fd.askopenfilename(
            title='Выберите аудиофайл',
            filetypes=(('Audio files', '*.mp3'), ('All files', '*.*'))
        )

        self.filename.set(filename)

    def update_albums(self, *args):
        """Обновление списка альбомов."""

        current_artist = self.artist_name_combobox.current()
        if current_artist == -1:
            albums = []
        else:
            albums = self.parent.session.get_albums(self.artist_ids[self.artist_name_combobox.current()])
        album_names = tuple([a.name for a in albums])
        self.album_ids = tuple([a.id for a in albums])

        self.album_name_combobox.configure(values=album_names)

    def add_track(self):
        """Добавление композиции."""

        # TODO: save audio

        if len(self.genres) != 0:
            genre_ids = [self.genres[i].id for i in range(len(self.genres)) if self.selected_genres[i].get()]
        else:
            genre_ids = []

        success, message = self.parent.session.add_track(
            self.track_name.get(),
            '0' * 24,
            self.album_ids[self.album_name_combobox.current()],
            genre_ids
        )
        if success:
            self.parent.update()
            self.destroy()
            showinfo(title='Успех', message='Добавление композиции прошло успешно')
        else:
            showerror(title='Ошибка добавления композиции', message=message)
