import pandas as pd
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
import json

class SelecionarPlanilhaScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.caminho_planilha = tk.StringVar()
        self.caminho_planilha.set('Nenhum arquivo selecionado')

        if os.path.exists('app_files/caminho_planilha.txt'):
            with open('app_files/caminho_planilha.txt', 'r', encoding='utf-8') as f:
                self.caminho_planilha.set(json.load(f))

        tk.Label(self, text='Planilha selecionada', font=('Arial', 16), width=25).pack(pady=30)

        self.text_widget = tk.Text(self, height=1, wrap='none', font=('Arial', 10), width=41)
        self.text_widget.insert('1.0', self.caminho_planilha.get())
        self.atualizar_nome_planilha()
        self.text_widget.configure(state='disabled')  
        self.text_widget.pack()

        scrollbar = tk.Scrollbar(self, orient='horizontal', command=self.text_widget.xview)
        scrollbar.pack(fill='x')
        self.text_widget.configure(xscrollcommand=scrollbar.set)

        tk.Button(self, text='Mudar', command=self.abrir_selecionador_arquivo, width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Voltar', command=lambda: controller.show_frame('ConfigScreen'), width=25, font=('Arial', 11)).pack(pady=10)

    def atualizar_nome_planilha(self):
        self.text_widget.configure(state='normal')
        self.text_widget.delete('1.0', 'end')
        self.text_widget.insert('1.0', self.caminho_planilha.get())
        self.text_widget.configure(state='disabled')

    def abrir_selecionador_arquivo(self):
        filepath = filedialog.askopenfilename(filetypes=[('Planilha Excel', '.xlsx')])

        if not filepath:
            return

        df = pd.read_excel(filepath)

        if not df.shape[1] == 2:
            messagebox.showerror(
                title='Erro!',
                message='PLANILHA - A planilha deve conter duas colunas: a primeira para alta e a segunda para a baixa.')
            return

        self.caminho_planilha.set(filepath)
        self.atualizar_nome_planilha()

        with open("app_files/caminho_planilha.txt", "w", encoding="utf-8") as f:
            json.dump(self.caminho_planilha.get(), f, ensure_ascii=False)
    
    
