import tkinter as tk
from screens.home import HomeScreen
from screens.config import ConfigScreen
from screens.selecionar_planilha import SelecionarPlanilhaScreen
from screens.selecionar_diretorio_download import SelecionarDiretorioDownload

class App(tk.Tk):
    ENVIRONMENT = 'PROD'

    def __init__(self):
        super().__init__()
        self.title('Transfer Arquivos Extra')
        self.geometry('300x350')
        self.maxsize(300, 350)
        self.minsize(300, 350)

        container = tk.Frame(self)
        container.pack()

        self.frames = {}

        # Add all screens here
        for F in (HomeScreen, ConfigScreen, SelecionarPlanilhaScreen, SelecionarDiretorioDownload):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky='nsew')

        self.show_frame('HomeScreen')

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()