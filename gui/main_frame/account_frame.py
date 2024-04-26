import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror, showinfo


class AccountFrame(ttk.Frame):
    """Виджет редактирования данных аккаунта."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        padding = {'padx': 10, 'pady': 10}

        self.session = container.app.session

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=5)
        self.rowconfigure(5, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.login_label = ttk.Label(self, text='Логин:')
        self.login_label.grid(row=0, column=0, columnspan=2, **padding)

        self.login = tk.StringVar()
        self.login_entry = ttk.Entry(self, textvariable=self.login)
        self.login_entry.configure(state='disabled')
        self.login_entry.grid(row=0, column=2, **padding)

        self.password_label = ttk.Label(self, text='Пароль:')
        self.password_label.grid(row=1, column=0, columnspan=2, **padding)

        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(self, textvariable=self.password, show='*')
        self.password_entry.grid(row=1, column=2, **padding)

        self.password_repeat_label = ttk.Label(self, text='Повторите пароль:')
        self.password_repeat_label.grid(row=2, column=0, columnspan=2, **padding)

        self.password_repeat = tk.StringVar()
        self.password_repeat_entry = ttk.Entry(self, textvariable=self.password_repeat, show='*')
        self.password_repeat_entry.grid(row=2, column=2, **padding)

        self.username_label = ttk.Label(self, text='Имя пользователя:')
        self.username_label.grid(row=3, column=0, columnspan=2, **padding)

        self.username = tk.StringVar()
        self.username_entry = ttk.Entry(self, textvariable=self.username)
        self.username_entry.grid(row=3, column=2, **padding)

        self.bio_label = ttk.Label(self, text='Биография:')
        self.bio_label.grid(row=4, column=0, **padding)

        self.bio_entry = tk.Text(self, width=40, height=5)
        self.bio_entry.grid(row=4, column=1, columnspan=2, **padding)

        self.save_button = ttk.Button(self, text='Сохранить', command=self.save_changes)
        self.save_button.grid(row=5, column=0, columnspan=3, **padding)

    def reset(self) -> None:
        """Сброс состояния виджета."""

        self.login.set(self.session.user.login)
        self.password.set('')
        self.password_repeat.set('')
        self.username.set(self.session.user.username)
        self.bio_entry.delete('1.0', 'end')
        self.bio_entry.insert('1.0', self.session.user.bio)

    def save_changes(self):
        """Сохранение изменений."""

        password, username, bio = None, None, None

        if self.password.get() != '' or self.password_repeat.get() != '':
            if self.password.get() != self.password_repeat.get():
                showerror(title='Ошибка редактирования аккаунта', message='Пароли не совпадают')
                return
            elif len(self.password.get()) < 4 or len(self.password.get()) > 50:
                showerror(title='Ошибка редактирования аккаунта', message='Недопустимая длина пароля')
                return

            password = self.password.get()

        if self.username.get() == '':
            showerror(title='Ошибка редактирования аккаунта', message='Поле имени пользователя не заполнено')
            return
        elif len(self.username.get()) < 4 or len(self.username.get()) > 50:
            showerror(title='Ошибка редактирования аккаунта', message='Недопустимая длина имени пользователя')
            return
        elif self.username.get() != self.session.user.username:
            username = self.username.get()

        if len(self.bio_entry.get('1.0', 'end')) > 1000:
            showerror(title='Ошибка редактирования аккаунта', message='Недопустимая длина биографии')
            return
        elif self.bio_entry.get('1.0', 'end') != self.session.user.bio:
            bio = self.bio_entry.get('1.0', 'end')

        success, message = self.session.edit_account(password, username, bio)
        if success:
            self.reset()
            showinfo(title='Успех', message='Изменения сохранены')
        else:
            showerror(title='Ошибка редактирования профиля', message=message)
