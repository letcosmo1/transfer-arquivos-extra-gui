import tkinter as tk
from tkinter import messagebox
import os
import time
import subprocess
import webbrowser

class HomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text='Transfer Arquivos Extra', font=('Arial', 16), width=25).pack(pady=20)
        tk.Button(self, text='Start', command=self.run_transfer_automation, width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Config', command=lambda: controller.show_frame('ConfigScreen'), width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Ajuda', command=lambda: webbrowser.open('https://github.com/letcosmo1/transfer-arquivos-extra-gui'), width=25, font=('Arial', 11)).pack(pady=10)

    def run_transfer_automation(self):
        if not os.path.exists('app_files/caminho_download.txt'):
            messagebox.showwarning(title='Atenção!',message='CONFIG - Configure o diretório de download.')
            return
        
        if not os.path.exists('app_files/caminho_planilha.txt'):
            messagebox.showwarning(title='Atenção!',message='CONFIG - Selecione a planilha de entrada.')
            return

        if not os.path.exists('app_files/coordenadas.txt'):
            messagebox.showwarning(title='Atenção!',message='CONFIG - Mapear transferência sucesso pendente.')
            return
        
        if not os.path.exists('app_files/coordenadas_erro.txt'):
            messagebox.showwarning(title='Atenção!',message='CONFIG - Mapear transferência com erro pendente.')
            return

        resposta = messagebox.askquestion(
            title='Confirme o início', 
            message='Posicione a tela no painel de transferência do mainframe. Pressione ESC para interromper a automação. Preparado para iniciar? ')
        
        if resposta == 'no': 
            return

        self.controller.iconify()

        time.sleep(1)

        if self.controller.ENVIRONMENT == 'PROD':
            subprocess.Popen([os.path.join("scripts", "automacao_transferencia.exe")])
        else:
            subprocess.Popen(["python", "scripts_automacao/automacao_transferencia.py"])

        
        

        


        