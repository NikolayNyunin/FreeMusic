import tkinter as tk

from session import MusicSession
from gui.login_frame import LoginFrame


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

        self.session = MusicSession()

        self.login_frame = LoginFrame(self)
        self.login_frame.grid(row=0, column=0)

    def show_login_frame(self):
        """Отображение виджета входа в аккаунт."""

        self.login_frame.reset()
        self.login_frame.tkraise()

    def show_sign_up_frame(self):
        """Отображение виджета создания аккаунта."""

        # TODO: implement

    def show_main_frame(self):
        """Отображение основного виджета приложения."""

        # TODO: implement
