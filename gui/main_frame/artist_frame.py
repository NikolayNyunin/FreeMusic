import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, showerror


class ArtistFrame(ttk.Frame):
    """Виджет отображения и редактирования списка исполнителей."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        self.padding = {'padx': 10, 'pady': 10}

        self.session = container.app.session

        self.add_artist_button = None

    def update(self) -> None:
        """Обновление состояния виджета."""

        # удаление всех дочерних виджетов
        for child in self.winfo_children():
            child.destroy()

        # если пользователь администратор
        # создание кнопки добавления исполнителя
        # if self.session.user is not None:
        #     if self.session.user.is_admin:
        self.add_artist_button = ttk.Button(self, text='Добавить исполнителя', command=self.show_add_artist_window)
        self.add_artist_button.pack(side='top', **self.padding)

        # отображение списка исполнителей
        for artist in self.session.get_all_artists():
            artist_frame = ttk.Frame(self)

            name_label = ttk.Label(artist_frame, text=artist.name)
            name_label.grid(row=0, column=0)

            description_label = ttk.Label(artist_frame, text=artist.description)
            description_label.grid(row=0, column=1)

            # if self.session.user is not None:
            #     if self.session.user.is_admin:
            delete_button = ttk.Button(artist_frame, text='Удалить',
                                       command=lambda artist_id=artist.id: self.delete_artist(artist_id))
            delete_button.grid(row=0, column=2, **self.padding)

            artist_frame.pack(side='top', **self.padding)

    def show_add_artist_window(self) -> None:
        """Отображение окна добавления исполнителя."""

        add_artist_window = AddArtistWindow(self)
        add_artist_window.grab_set()

    def delete_artist(self, artist_id: int) -> None:
        """Удаление исполнителя."""

        # подтверждение удаления исполнителя
        confirmation = askokcancel(
            title='Подтверждение удаления исполнителя',
            message='Вы уверены, что хотите безвозвратно удалить исполнителя?',
            icon='warning'
        )
        if not confirmation:
            return

        # попытка удаления исполнителя
        success, message = self.session.delete_artist(artist_id)
        if success:
            self.update()
            showinfo(title='Успех', message='Удаление исполнителя прошло успешно')
        else:
            showerror(title='Ошибка удаления исполнителя', message=message)


class AddArtistWindow(tk.Toplevel):
    """Окно добавления исполнителей."""

    def __init__(self, parent):
        """Инициализация окна."""

        super().__init__(parent)

        padding = {'padx': 10, 'pady': 10}

        self.parent = parent

        self.geometry('540x280')
        self.title('Добавление исполнителя')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure(3, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.artist_name_label = ttk.Label(self, text='Название исполнителя:')
        self.artist_name_label.grid(row=0, column=0, columnspan=2, **padding)

        self.artist_name = tk.StringVar()
        self.artist_name_entry = ttk.Entry(self, textvariable=self.artist_name)
        self.artist_name_entry.grid(row=0, column=2, **padding)

        self.artist_description_label = ttk.Label(self, text='Описание/биография:')
        self.artist_description_label.grid(row=1, column=0, **padding)

        self.artist_description_entry = tk.Text(self, width=40, height=8)
        self.artist_description_entry.grid(row=1, column=1, columnspan=2, **padding)

        self.add_artist_button = ttk.Button(self, text='Создать исполнителя', command=self.add_artist)
        self.add_artist_button.grid(row=2, column=0, columnspan=3, **padding)

    def add_artist(self):
        """Добавление исполнителя."""

        success, message = self.parent.session.add_artist(
            self.artist_name.get(),
            self.artist_description_entry.get('1.0', 'end')
        )
        if success:
            self.parent.update()
            self.destroy()
            showinfo(title='Успех', message='Добавление исполнителя прошло успешно')
        else:
            showerror(title='Ошибка добавления исполнителя', message=message)
