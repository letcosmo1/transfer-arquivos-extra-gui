import pyautogui
from pynput import mouse
import json

terminate = False
ignore_first_click = False
clicked_position = None

steps = [
    { 'componente':'Ícone da pasta', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Item da lista de transferência', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Input do arquivo da baixa', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Input do arquivo da alta', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Botão Aplicar', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Botão Transferir', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Botão Sim', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Botão Ok', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Botão Ok final', 'coordenadas': { 'x':0, 'y':0 } },
]

def on_click(x, y, pressed):
    global ignore_first_click, clicked_position

    if pressed:
        # Ignore the first click (the dialog button press)
        if ignore_first_click:
            ignore_first_click = False
            return 

        # Stop listener
        clicked_position = (x, y)
        return False
    
for step in steps:
    resposta = pyautogui.confirm(
        title='Clique no componente',
        text=f'Clique no "{step['componente']}"', 
        buttons=['Ok', 'Cancelar'])
        
    if resposta == 'Cancelar' or resposta == None:
        terminate = True
        break

    if(resposta == 'Ok'):
        # Collect events until released
        with mouse.Listener(on_click=on_click,) as listener:
            listener.join()

        while True:
            resposta = pyautogui.confirm(
                title=f'Confirme as coordenadas {clicked_position}', 
                text=f'Você clicou no "{step['componente']}"?', 
                buttons=['Sim', 'Tentar de novo'])
            
            if resposta == 'Tentar de novo':
                # Ignore the first click (the dialog button press)
                ignore_first_click = True  
                with mouse.Listener(on_click=on_click,) as listener:
                    listener.join()
            elif resposta == 'Sim':
                x, y = clicked_position
                step['coordenadas']['x'] = x
                step['coordenadas']['y'] = y
                break
            else:
                terminate = True
                break

if(not terminate):
    with open("app_files/coordenadas.txt", "w", encoding="utf-8") as f:
        json.dump(steps, f, ensure_ascii=False)



    
    






        



    







