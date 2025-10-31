import pyautogui
from pynput import mouse
import json

terminate = False
ignore_first_click = False
clicked_position = None

steps_erro = [
    { 'componente':'Botão fechar', 'coordenadas': { 'x':0, 'y':0 } },
    { 'componente':'Botão Ok', 'coordenadas': { 'x':0, 'y':0 } },
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
    
for step in steps_erro:
    resposta = pyautogui.confirm(
        title='Clique no componente',
        text=f'Clique no "{step['componente']}"', 
        buttons=['Ok', 'Cancelar'])
    
    if resposta == 'Cancelar' or resposta == None:
        terminate = True
        break

    if(resposta == 'Ok'):
        with mouse.Listener(on_click=on_click,) as listener:
            listener.join()

        while True:
            resposta = pyautogui.confirm(
                title=f'Confirme as coordenadas {clicked_position}', 
                text=f'Você clicou no "{step['componente']}"?', 
                buttons=['Sim', 'Tentar de novo'])
            
            if(resposta == 'Tentar de novo'):
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
    with open("app_files/coordenadas_erro.txt", "w", encoding="utf-8") as f:
        json.dump(steps_erro, f, ensure_ascii=False)