import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showerror


class LoginFrame(ttk.Frame):
    """Виджет входа в аккаунт."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        padding = {'padx': 20, 'pady': 10}

        self.app = container

        self.login_form = ttk.Frame(self)

        self.login_label = ttk.Label(self.login_form, text='Логин:')
        self.login_label.grid(row=0, column=0, **padding)

        self.login = tk.StringVar()
        self.login_entry = ttk.Entry(self.login_form, textvariable=self.login, font=self.app.FONT, width=20)
        self.login_entry.grid(row=0, column=1, **padding)

        self.password_label = ttk.Label(self.login_form, text='Пароль:')
        self.password_label.grid(row=1, column=0, **padding)

        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(self.login_form, textvariable=self.password, show='*',
                                        font=self.app.FONT, width=20)
        self.password_entry.grid(row=1, column=1, **padding)

        self.login_button = ttk.Button(self.login_form, text='Войти', command=self.attempt_login)
        self.login_button.grid(row=3, columnspan=2, **padding)

        self.login_form.pack(pady=(220, 0))

        self.sign_up_button = ttk.Button(self, text='Нет аккаунта? Зарегистрироваться.',
                                         command=self.app.show_sign_up_frame)
        self.sign_up_button.pack()

    def reset(self) -> None:
        """Очистка полей виджета."""

        self.login.set('')
        self.password.set('')

    def attempt_login(self) -> None:
        """Попытка входа в аккаунт."""

        # первичная проверка правильности заполнения полей ввода
        if self.login.get() == '':
            showerror(title='Ошибка входа', message='Поле логина не заполнено')
            return
        elif len(self.login.get()) < 4 or len(self.login.get()) > 50:
            showerror(title='Ошибка входа', message='Недопустимая длина логина')
            return
        elif self.password.get() == '':
            showerror(title='Ошибка входа', message='Поле пароля не заполнено')
            return
        elif len(self.password.get()) < 4 or len(self.password.get()) > 50:
            showerror(title='Ошибка входа', message='Недопустимая длина пароля')
            return

        # вход в аккаунт
        success, message = self.app.session.login(self.login.get(), self.password.get())
        if success:
            self.app.show_main_frame()
        else:
            showerror(title='Ошибка входа', message=message)
