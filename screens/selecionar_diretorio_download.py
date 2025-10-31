import tkinter as tk
from tkinter import filedialog
import os
import json

class SelecionarDiretorioDownload(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.caminho_download = tk.StringVar()
        self.caminho_download.set('Nenhum diretório selecionado')

        if os.path.exists('app_files/caminho_download.txt'):
            with open('app_files/caminho_download.txt', 'r', encoding='utf-8') as f:
                self.caminho_download.set(json.load(f))

        tk.Label(self, text='Diretório de download selecionado', font=('Arial', 14), width=27, wraplength=200).pack(pady=30)

        self.text_widget = tk.Text(self, height=1, wrap='none', font=('Arial', 10), width=41)
        self.text_widget.insert('1.0', self.caminho_download.get())
        self.atualizar_nome_diretorio()
        self.text_widget.configure(state='disabled')  
        self.text_widget.pack()

        scrollbar = tk.Scrollbar(self, orient='horizontal', command=self.text_widget.xview)
        scrollbar.pack(fill='x')
        self.text_widget.configure(xscrollcommand=scrollbar.set)

        tk.Button(self, text='Mudar', command=self.abrir_selecionador_arquivo, width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Voltar', command=lambda: controller.show_frame('ConfigScreen'), width=25, font=('Arial', 11)).pack(pady=10)

    def atualizar_nome_diretorio(self):
        self.text_widget.configure(state='normal')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', self.caminho_download.get())
        self.text_widget.configure(state='disabled')

    def abrir_selecionador_arquivo(self):
        filepath = filedialog.askdirectory()
        self.caminho_download.set(filepath)
        self.atualizar_nome_diretorio()

        with open("app_files/caminho_download.txt", "w", encoding="utf-8") as f:
            json.dump(self.caminho_download.get(), f, ensure_ascii=False)
    
    
