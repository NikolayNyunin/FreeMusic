import tkinter as tk
from tkinter import ttk


class App(tk.Tk):
    """Основной класс приложения."""

    def __init__(self):
        """Инициализация основного окна приложения."""

        super().__init__()

        self.title('Free Music')
        self.geometry('1080x720')
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.login_frame = LoginFrame(self)
        self.login_frame.grid(row=0, column=0)


class LoginFrame(ttk.Frame):
    """Виджет входа в аккаунт."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        padding = {'padx': 10, 'pady': 5}

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

        self.login_button = ttk.Button(self.login_form, text='Войти')
        self.login_button.grid(row=3, columnspan=2, **padding)

        self.login_form.pack()
