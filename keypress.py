from pywinauto.application import Application
from pywinauto.keyboard import send_keys
from pywinauto.mouse import click
import json
import time
import logging


with open('PATH.json', 'r') as config_file:
    config = json.load(config_file)

game_path = config["game_path"]
pytesseract_path = config["pytesseract_path"]
debug_path = config["debug_path"]
alert_sound_path = config["alert_sound_path"] 
folder_path = config["folder_path"]  
template_path = config["template_path"] 


logging.basicConfig(filename="pywinauto.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)




def initialize():
    app = Application(backend="win32").connect(path=game_path)
    dlg_spec = app.window(title='Tower Unite')
    print(dlg_spec)
    logging.info(dlg_spec)
    while not app.windows():
        time.sleep(.5)
        print("insleep\n")

    click(button='left', coords=(150, 150))
    time.sleep(1.5)


    send_keys("{3 down}")
    time.sleep(0.5)
    send_keys("{3 up}")
    logging.info("Initialization Complete")



def space():
    send_keys("{SPACE}")
    time.sleep(5.5)


def response(answer):
    time.sleep(2.5)
    keycompose_down = str("{"+answer+" down}")
    keycompose_up = str("{"+answer+" up}")
    send_keys(keycompose_down)
    time.sleep(0.5)
    send_keys(keycompose_up)