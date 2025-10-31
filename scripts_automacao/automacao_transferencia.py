import pyautogui
import time
import os
import pandas as pd
import json
from pynput import keyboard

def automacao_transferencia(steps, steps_erro, arquivo_alta, arquivo_baixa, diretorio_receber):
    global stop_script, arquivos_com_erro

    if not stop_script:
        #clicar icone pasta
        pyautogui.click(x=steps[0]['coordenadas']['x'], y=steps[0]['coordenadas']['y'])

    if not stop_script:
        time.sleep(3)
        #clicar no item da lista de transferencia
        pyautogui.click(x=steps[1]['coordenadas']['x'], y=steps[1]['coordenadas']['y'])

    if not stop_script:
        #alterar o nome do arquivo a receber na baixa
        pyautogui.click(x=steps[2]['coordenadas']['x'], y=steps[2]['coordenadas']['y'])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write(os.path.join(diretorio_receber, arquivo_baixa) + '.txt')

    if not stop_script:
        #alterar o nome do arquivo a enviar da alta
        pyautogui.click(x=steps[3]['coordenadas']['x'], y=steps[3]['coordenadas']['y'])
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        pyautogui.write("'" + arquivo_alta + "'")

    if not stop_script:
        #clicar no botao aplicar
        pyautogui.click(x=steps[4]['coordenadas']['x'], y=steps[4]['coordenadas']['y'])

    if not stop_script:
        #clicar no botao transferir
        pyautogui.click(x=steps[5]['coordenadas']['x'], y=steps[5]['coordenadas']['y'])

    if not stop_script:
        time.sleep(1)
        #clicar no botão sim
        pyautogui.click(x=steps[6]['coordenadas']['x'], y=steps[6]['coordenadas']['y'])

    if not stop_script:
        time.sleep(1)
        #clicar no botão ok
        pyautogui.click(x=steps[7]['coordenadas']['x'], y=steps[7]['coordenadas']['y'])

    if not stop_script:
        time.sleep(1)
        #verifica existencia do arquivo
        while not os.path.exists(os.path.join(diretorio_receber, arquivo_baixa) + '.txt'):
            if stop_script:
                break
            time.sleep(1)
    
    if not stop_script:
        #verificar conclusão da transferencia
        tamanho_anterior = -1
        while True:
            try:
                if stop_script:
                    break
                tamanho_arquivo = os.path.getsize(os.path.join(diretorio_receber, arquivo_baixa) + '.txt')
            except FileNotFoundError:
                arquivos_com_erro.append(arquivo_alta)

                if not stop_script:
                    time.sleep(3)
                    #clicar no botão fechar
                    pyautogui.click(x=steps_erro[0]['coordenadas']['x'], y=steps_erro[0]['coordenadas']['y'])

                if not stop_script:
                    time.sleep(1)
                    #clicar no botão ok
                    pyautogui.click(x=steps_erro[1]['coordenadas']['x'], y=steps_erro[1]['coordenadas']['y'])

                if not stop_script:
                    time.sleep(1)
                    #apertar enter
                    pyautogui.press('enter')
                    time.sleep(2)

                return

            if tamanho_arquivo == tamanho_anterior:
                if tamanho_arquivo != 0:
                    break

            tamanho_anterior = tamanho_arquivo
            time.sleep(1)

    if not stop_script:
        time.sleep(2)
        #fechar janela conclusao
        pyautogui.click(x=steps[8]['coordenadas']['x'], y=steps[8]['coordenadas']['y'])

def abrir_arquivos():
    with open("app_files/caminho_download.txt", "r", encoding="utf-8") as f:
        diretorio_receber = os.path.normpath(json.load(f))

    with open("app_files/caminho_planilha.txt", "r", encoding="utf-8") as f:
        diretorio_planilha = os.path.normpath(json.load(f))

    with open("app_files/coordenadas.txt", "r", encoding="utf-8") as f:
        steps = json.load(f)

    with open("app_files/coordenadas_erro.txt", "r", encoding="utf-8") as f:
        steps_erro = json.load(f)
    
    return diretorio_receber, diretorio_planilha, steps, steps_erro

def converter_planilha():
    try:
        df = pd.read_excel(diretorio_planilha)
    except Exception as e:
        pyautogui.alert(f'AUTO - Erro ao acessar a planilha de entrada. {str(e)}', 'Erro')
        raise 
    
    tuplas_arquivos = list(df.itertuples(index=False, name=None))
    return tuplas_arquivos

def on_press(key):
    global stop_script, running
    try:
        if key == keyboard.Key.esc:
            if running == True:
                stop_script = True
            # Stop the listener
            return False

    except AttributeError:
        pass

stop_script = False
running = True
arquivos_com_erro = []

# Start the keyboard listener in the background
listener = keyboard.Listener(on_press=on_press)
listener.start()

diretorio_receber, diretorio_planilha, steps, steps_erro = abrir_arquivos()
tuplas_arquivos = converter_planilha()

for nome_arquivo_alta, nome_arquivo_baixa in tuplas_arquivos:
    if stop_script:
        break

    automacao_transferencia(
        steps, 
        steps_erro, 
        nome_arquivo_alta, 
        nome_arquivo_baixa, 
        diretorio_receber)

time.sleep(1)
running = False
pyautogui.press('esc')

if stop_script:
    pyautogui.alert('Automação interrompida.', 'Interrompição')
else:
    pyautogui.alert('\n'.join(arquivos_com_erro), 'Arquivos não transferidos')
    pyautogui.alert('Automação concluída com sucesso.', 'Concluído')


