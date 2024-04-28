import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from session import MusicSession
from gui.login_frame import LoginFrame
from gui.sign_up_frame import SignUpFrame
from gui.main_frame.main_frame import MainFrame


class App(tk.Tk):
    """Основной класс приложения."""

    FONT = 'Helvetica 12'
    HEADER_FONT = 'Helvetica 14 bold'

    def __init__(self):
        """Инициализация основного окна приложения."""

        super().__init__()

        self.title('Free Music')
        self.geometry('1080x720')
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.session = MusicSession()

        add_image = Image.open('img/add.png')
        self.add_image = ImageTk.PhotoImage(add_image.resize((60, 60)))

        delete_image = Image.open('img/delete.png')
        self.delete_image = ImageTk.PhotoImage(delete_image.resize((40, 40)))

        self.login_frame = LoginFrame(self)
        self.login_frame.grid(row=0, column=0, sticky='nsew')

        self.sign_up_frame = SignUpFrame(self)
        self.sign_up_frame.grid(row=0, column=0, sticky='nsew')

        self.main_frame = MainFrame(self)
        self.main_frame.grid(row=0, column=0, sticky='nsew')

        self.configure_style()

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

    def configure_style(self):
        """Настройка стиля приложения."""

        style = ttk.Style(self)
        style.configure('TLabel', font=self.FONT)
        style.configure('TButton', font=self.FONT)
        style.configure('TCheckbutton', font=self.FONT)
