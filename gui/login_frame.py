import tkinter as tk
from tkinter import ttk


class LoginFrame(ttk.Frame):
    """Виджет входа в аккаунт."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        padding = {'padx': 10, 'pady': 5}

        self.app = container

        self.login_error = tk.StringVar()
        self.login_error_label = ttk.Label(self, textvariable=self.login_error, foreground='red')
        self.login_error_label.pack()

        self.login_form = ttk.Frame(self)

        self.login_label = ttk.Label(self.login_form, text='Логин:')
        self.login_label.grid(row=0, column=0, **padding)

        self.login = tk.StringVar()
        self.login_entry = ttk.Entry(self.login_form, textvariable=self.login)
        self.login_entry.grid(row=0, column=1, **padding)

        self.password_label = ttk.Label(self.login_form, text='Пароль:')
        self.password_label.grid(row=1, column=0, **padding)

        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(self.login_form, textvariable=self.password, show='*')
        self.password_entry.grid(row=1, column=1, **padding)

        self.login_button = ttk.Button(self.login_form, text='Войти', command=self.attempt_login)
        self.login_button.grid(row=3, columnspan=2, **padding)

        self.login_form.pack()

        self.sign_up_button = ttk.Button(self, text='Нет аккаунта? Зарегистрироваться.',
                                         command=self.app.show_sign_up_frame)
        self.sign_up_button.pack()

    def reset(self) -> None:
        """Очистка полей виджета."""

        self.login_error.set('')
        self.login.set('')
        self.password.set('')

    def attempt_login(self) -> None:
        """Попытка входа в аккаунт."""

        # первичная проверка правильности заполнения полей ввода
        if self.login.get() == '':
            self.login_error.set('Empty login field')
            return
        elif self.password.get() == '':
            self.login_error.set('Empty password field')
            return

        # вход в аккаунт
        success, message = self.app.session.login(self.login.get(), self.password.get())
        if success:
            self.app.show_main_frame()
        else:
            self.login_error.set(message)
