import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror


class SignUpFrame(ttk.Frame):
    """Виджет регистрации нового аккаунта."""

    def __init__(self, container):
        """Инициализация виджета."""

        super().__init__(container)

        padding = {'padx': 10, 'pady': 5}

        self.app = container

        self.sign_up_form = ttk.Frame(self)

        self.login_label = ttk.Label(self.sign_up_form, text='Логин (уникальный):')
        self.login_label.grid(row=0, column=0, **padding)

        self.login = tk.StringVar()
        self.login_entry = ttk.Entry(self.sign_up_form, textvariable=self.login)
        self.login_entry.grid(row=0, column=1, **padding)

        self.password_label = ttk.Label(self.sign_up_form, text='Пароль:')
        self.password_label.grid(row=1, column=0, **padding)

        self.password = tk.StringVar()
        self.password_entry = ttk.Entry(self.sign_up_form, textvariable=self.password, show='*')
        self.password_entry.grid(row=1, column=1, **padding)

        self.password_repeat_label = ttk.Label(self.sign_up_form, text='Повторите пароль:')
        self.password_repeat_label.grid(row=2, column=0, **padding)

        self.password_repeat = tk.StringVar()
        self.password_repeat_entry = ttk.Entry(self.sign_up_form, textvariable=self.password_repeat, show='*')
        self.password_repeat_entry.grid(row=2, column=1, **padding)

        self.username_label = ttk.Label(self.sign_up_form, text='Имя пользователя:')
        self.username_label.grid(row=3, column=0, **padding)

        self.username = tk.StringVar()
        self.username_entry = ttk.Entry(self.sign_up_form, textvariable=self.username)
        self.username_entry.grid(row=3, column=1, **padding)

        self.bio_label = ttk.Label(self.sign_up_form, text='Биография:')
        self.bio_label.grid(row=4, column=0, **padding)

        self.bio_entry = tk.Text(self.sign_up_form, width=40, height=5)
        self.bio_entry.grid(row=4, column=1, **padding)

        self.sign_up_button = ttk.Button(self.sign_up_form, text='Зарегистрироваться', command=self.attempt_sign_up)
        self.sign_up_button.grid(row=5, columnspan=2, **padding)

        self.sign_up_form.pack()

        self.login_button = ttk.Button(self, text='Уже есть аккаунт? Войти.',
                                       command=self.app.show_login_frame)
        self.login_button.pack()

    def reset(self) -> None:
        """Очистка полей виджета."""

        self.login.set('')
        self.password.set('')
        self.password_repeat.set('')
        self.username.set('')
        self.bio_entry.delete('1.0', tk.END)

    def attempt_sign_up(self) -> None:
        """Попытка регистрации нового аккаунта."""

        # первичная проверка правильности заполнения полей ввода
        if self.login.get() == '':
            showerror(title='Ошибка регистрации', message='Поле логина не заполнено')
            return
        elif len(self.login.get()) < 4 or len(self.login.get()) > 50:
            showerror(title='Ошибка регистрации', message='Недопустимая длина логина')
            return
        elif self.password.get() == '':
            showerror(title='Ошибка регистрации', message='Поле пароля не заполнено')
            return
        elif self.password_repeat.get() == '':
            showerror(title='Ошибка регистрации', message='Поле повтора пароля не заполнено')
            return
        elif self.password.get() != self.password_repeat.get():
            showerror(title='Ошибка регистрации', message='Пароли не совпадают')
            return
        elif len(self.password.get()) < 4 or len(self.password.get()) > 50:
            showerror(title='Ошибка регистрации', message='Недопустимая длина пароля')
            return
        elif self.username.get() == '':
            showerror(title='Ошибка регистрации', message='Поле имени пользователя не заполнено')
            return
        elif len(self.username.get()) < 4 or len(self.username.get()) > 50:
            showerror(title='Ошибка регистрации', message='Недопустимая длина имени пользователя')
            return

        # регистрация нового аккаунта
        success, message = self.app.session.sign_up(
            self.login.get(),
            self.password.get(),
            self.username.get(),
            self.bio_entry.get('1.0', 'end')
        )
        if success:
            self.app.show_login_frame()
            showinfo(title='Успех', message='Регистрация прошла успешно')
        else:
            showerror(title='Ошибка регистрации', message=message)
