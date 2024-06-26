import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, showerror
from tkcalendar import DateEntry


class AlbumFrame(ttk.Frame):
    """Виджет отображения и редактирования списка альбомов."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        self.padding = {'padx': 10, 'pady': 20}

        self.app = container.app
        self.session = self.app.session

        self.add_album_button = None
        self.no_albums_label = None
        self.albums_frame = None

    def update(self) -> None:
        """Обновление состояния виджета."""

        # удаление всех дочерних виджетов
        for child in self.winfo_children():
            child.destroy()

        # получение списка добавленных альбомов
        albums = self.session.get_all_albums()

        if len(albums) == 0:  # если пока не добавлено ни одного альбома
            self.no_albums_label = ttk.Label(self, text='Пока не добавлено ни одного альбома',
                                             font='Helvetica 16')
            self.no_albums_label.pack(pady=(150, 0))
        else:  # заполнение шапки таблицы
            self.albums_frame = ttk.Frame(self)

            self.albums_frame.columnconfigure(0, weight=2)
            self.albums_frame.columnconfigure(1, weight=2)
            self.albums_frame.columnconfigure(2, weight=2)
            self.albums_frame.columnconfigure(3, weight=1)

            name_label = ttk.Label(self.albums_frame, text='Название', font=self.app.HEADER_FONT)
            name_label.grid(row=0, column=0)

            release_date_label = ttk.Label(self.albums_frame, text='Дата выхода', font=self.app.HEADER_FONT)
            release_date_label.grid(row=0, column=1)

            artist_name_label = ttk.Label(self.albums_frame, text='Исполнитель', font=self.app.HEADER_FONT)
            artist_name_label.grid(row=0, column=2)

            self.albums_frame.pack(side='top', fill='x', **self.padding)

        # отображение списка альбомов
        for i, album in enumerate(albums):
            separator = ttk.Separator(self.albums_frame, orient='horizontal')
            separator.grid(row=2 * i + 1, column=0, columnspan=4, sticky='nsew', pady=10)

            name_label = ttk.Label(self.albums_frame, text=album.name)
            name_label.grid(row=2 * i + 2, column=0)

            release_date_label = ttk.Label(self.albums_frame, text=album.release_date.strftime('%d-%m-%Y'))
            release_date_label.grid(row=2 * i + 2, column=1)

            artist_name_label = ttk.Label(self.albums_frame, text=self.session.get_artist(album.artist_id).name)
            artist_name_label.grid(row=2 * i + 2, column=2)

            if self.session.user is not None:
                if self.session.user.is_admin:
                    delete_button = ttk.Button(self.albums_frame, image=self.app.delete_image,
                                               command=lambda album_id=album.id: self.delete_album(album_id))
                    delete_button.grid(row=2 * i + 2, column=3)

        # если пользователь администратор
        # создание кнопки добавления альбома
        if self.session.user is not None:
            if self.session.user.is_admin:
                self.add_album_button = ttk.Button(self, image=self.app.add_image,
                                                   command=self.show_add_album_window)
                self.add_album_button.pack(side='top', **self.padding)

    def show_add_album_window(self) -> None:
        """Отображение окна добавления альбома."""

        add_album_window = AddAlbumWindow(self)
        add_album_window.grab_set()

    def delete_album(self, album_id: int) -> None:
        """Удаление альбома."""

        # подтверждение удаления альбома
        confirmation = askokcancel(
            title='Подтверждение удаления альбома',
            message='Вы уверены, что хотите безвозвратно удалить альбом?',
            icon='warning'
        )
        if not confirmation:
            return

        # попытка удаления альбома
        success, message = self.session.delete_album(album_id)
        if success:
            self.update()
            showinfo(title='Успех', message='Удаление альбома прошло успешно')
        else:
            showerror(title='Ошибка удаления альбома', message=message)


class AddAlbumWindow(tk.Toplevel):
    """Окно добавления альбома."""

    def __init__(self, parent):
        """Инициализация окна."""

        super().__init__(parent)

        padding = {'padx': 10, 'pady': 10}

        self.parent = parent

        self.geometry('540x280')
        self.title('Добавление альбома')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.album_name_label = ttk.Label(self, text='Название альбома:')
        self.album_name_label.grid(row=0, column=0, **padding)

        self.album_name = tk.StringVar()
        self.album_name_entry = ttk.Entry(self, textvariable=self.album_name,
                                          font=self.parent.app.FONT, width=25)
        self.album_name_entry.grid(row=0, column=1, **padding)

        self.release_date_label = ttk.Label(self, text='Дата выхода:')
        self.release_date_label.grid(row=1, column=0, **padding)

        self.release_date_entry = DateEntry(self, date_pattern='dd/mm/y', font=self.parent.app.FONT, width=10)
        self.release_date_entry.grid(row=1, column=1, **padding)

        self.artist_name_label = ttk.Label(self, text='Исполнитель:')
        self.artist_name_label.grid(row=2, column=0, **padding)

        # подготовка списка исполнителей для отображения
        artists = self.parent.session.get_all_artists()
        artist_names = tuple([a.name for a in artists])
        self.artist_ids = tuple([a.id for a in artists])

        self.artist_name = tk.StringVar()
        self.artist_name_combobox = ttk.Combobox(self, textvariable=self.artist_name, values=artist_names,
                                                 state='readonly', font=self.parent.app.FONT, width=25)
        self.artist_name_combobox.grid(row=2, column=1, **padding)

        self.add_album_button = ttk.Button(self, text='Добавить альбом', command=self.add_album)
        self.add_album_button.grid(row=3, column=0, columnspan=2, **padding)

    def add_album(self):
        """Добавление альбома."""

        if self.album_name.get() == '':
            showerror(title='Ошибка добавления альбома', message='Поле названия альбома не заполнено')
            return
        elif len(self.album_name.get()) < 4 or len(self.album_name.get()) > 50:
            showerror(title='Ошибка добавления альбома', message='Недопустимая длина названия альбома')
            return
        elif self.artist_name_combobox.current() == -1:
            showerror(title='Ошибка добавления альбома', message='Исполнитель не выбран')
            return

        success, message = self.parent.session.add_album(
            self.album_name.get(),
            self.release_date_entry.get_date(),
            self.artist_ids[self.artist_name_combobox.current()]
        )
        if success:
            self.parent.update()
            self.destroy()
            showinfo(title='Успех', message='Добавление альбома прошло успешно')
        else:
            showerror(title='Ошибка добавления альбома', message=message)
