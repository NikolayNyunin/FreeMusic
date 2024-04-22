import tkinter as tk

from session import MusicSession
from gui.login_frame import LoginFrame
from gui.sign_up_frame import SignUpFrame
from gui.main_frame.main_frame import MainFrame


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
        self.login_frame.grid(row=0, column=0, sticky='nsew')
        # self.login_frame.configure(padding=200)  # TODO: find a better solution

        self.sign_up_frame = SignUpFrame(self)
        self.sign_up_frame.grid(row=0, column=0, sticky='nsew')

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        self.show_login_frame()

    def show_login_frame(self):
        """Отображение виджета входа в аккаунт."""

        self.login_frame.reset()
        self.login_frame.tkraise()

    def show_sign_up_frame(self):
        """Отображение виджета создания аккаунта."""

        self.sign_up_frame.reset()
        self.sign_up_frame.tkraise()

    def show_main_frame(self):
        """Отображение основного виджета приложения."""

        self.main_frame.reset()
        self.main_frame.tkraise()
