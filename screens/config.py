import tkinter as tk
import subprocess
import os

class ConfigScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text='Config', font=('Arial', 16), width=25).pack(pady=20)
        tk.Button(self, text='Mapear sucesso', command=self.run_map_transfer, width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Mapear erro', command=self.run_map_error_script, width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Selecionar planilha', command=lambda: controller.show_frame('SelecionarPlanilhaScreen'), width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Selecionar diretório de download', command=lambda: controller.show_frame('SelecionarDiretorioDownload'), width=25, font=('Arial', 11)).pack(pady=10)
        tk.Button(self, text='Voltar', command=lambda: controller.show_frame('HomeScreen'), width=25, font=('Arial', 11)).pack(pady=10)
    
    def run_map_transfer(self):
        self.controller.iconify()
        if self.controller.ENVIRONMENT == 'PROD':
            subprocess.Popen([os.path.join("scripts", "mapear_transferencia.exe")])
        else:
            subprocess.Popen(["python", "scripts_mapeamento/mapear_transferenciao.py"])

    def run_map_error_script(self):
        self.controller.iconify()
        if self.controller.ENVIRONMENT == 'PROD':
            subprocess.Popen([os.path.join("scripts", "mapear_erro.exe")])
        else:
            subprocess.Popen(["python", "scripts_mapeamento/mapear_erro.py"])