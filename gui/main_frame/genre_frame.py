import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askokcancel, showinfo, showerror


class GenreFrame(ttk.Frame):
    """Виджет отображения и редактирования списка жанров."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        self.padding = {'padx': 10, 'pady': 10}

        self.session = container.app.session

        self.add_genre_button = None

    def update(self) -> None:
        """Обновление состояния виджета."""

        # удаление всех дочерних виджетов
        for child in self.winfo_children():
            child.destroy()

        # если пользователь администратор
        # создание кнопки добавления жанра
        # if self.session.user is not None:
        #     if self.session.user.is_admin:
        self.add_genre_button = ttk.Button(self, text='Добавить жанр', command=self.show_add_genre_window)
        self.add_genre_button.pack(side='top', **self.padding)

        # отображение списка жанров
        for genre in self.session.get_all_genres():
            genre_frame = ttk.Frame(self)

            name_label = ttk.Label(genre_frame, text=genre.name)
            name_label.grid(row=0, column=0, **self.padding)

            # if self.session.user is not None:
            #     if self.session.user.is_admin:
            delete_button = ttk.Button(genre_frame, text='Удалить',
                                       command=lambda genre_id=genre.id: self.delete_genre(genre_id))
            delete_button.grid(row=0, column=2, **self.padding)

            genre_frame.pack(side='top', **self.padding)

    def show_add_genre_window(self) -> None:
        """Отображение окна добавления жанра."""

        add_genre_window = AddGenreWindow(self)
        add_genre_window.grab_set()

    def delete_genre(self, genre_id: int) -> None:
        """Удаление жанра."""

        # подтверждение удаления жанра
        confirmation = askokcancel(
            title='Подтверждение удаления жанра',
            message='Вы уверены, что хотите безвозвратно удалить жанр?',
            icon='warning'
        )
        if not confirmation:
            return

        # попытка удаления жанра
        success, message = self.session.delete_genre(genre_id)
        if success:
            self.update()
            showinfo(title='Успех', message='Удаление жанра прошло успешно')
        else:
            showerror(title='Ошибка удаления жанра', message=message)


class AddGenreWindow(tk.Toplevel):
    """Окно добавления жанра."""

    def __init__(self, parent):
        """Инициализация окна."""

        super().__init__(parent)

        padding = {'padx': 10, 'pady': 10}

        self.parent = parent

        self.geometry('360x120')
        self.title('Добавление жанра')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.genre_name_label = ttk.Label(self, text='Название жанра:')
        self.genre_name_label.grid(row=0, column=0, **padding)

        self.genre_name = tk.StringVar()
        self.genre_name_entry = ttk.Entry(self, textvariable=self.genre_name)
        self.genre_name_entry.grid(row=0, column=1, **padding)

        self.add_genre_button = ttk.Button(self, text='Создать жанр', command=self.add_genre)
        self.add_genre_button.grid(row=1, column=0, columnspan=2, **padding)

    def add_genre(self):
        """Добавление жанра."""

        success, message = self.parent.session.add_genre(self.genre_name.get())
        if success:
            self.parent.update()
            self.destroy()
            showinfo(title='Успех', message='Добавление жанра прошло успешно')
        else:
            showerror(title='Ошибка добавления жанра', message=message)
