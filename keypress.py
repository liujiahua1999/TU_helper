from pywinauto.application import Application
import pywinauto.keyboard as keyboard
from pywinauto.mouse import click
import json
import time
import logging


with open('PATH.json', 'r') as config_file:
    config = json.load(config_file)


debug_path = config["debug_path"]
alert_sound_path = config["alert_sound_path"] 
folder_path = config["folder_path"]  
template_path = config["template_path"] 


logging.basicConfig(filename="pywinauto.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


app = Application(backend="win32").connect(path=r"E:\SteamLibrary\steamapps\common\Tower Unite\Tower\Binaries\Win64")
game_window = app['Tower Unite']

def initialize():
    app = Application(backend="win32").connect(path=r"E:\SteamLibrary\steamapps\common\Tower Unite\Tower\Binaries\Win64")
    game_window = app['Tower Unite']
    print(game_window)
    logging.info(game_window)
    while not app.windows():
        time.sleep(.5)
        print("insleep\n")

    #click(button='left', coords=(150, 150))
    time.sleep(1.5)


    game_window.send_keystrokes("{3}")
    time.sleep(0.5)

    logging.info("Initialization Complete")



def space():
    game_window.send_keystrokes("{SPACE}")
    time.sleep(5.5)
    print("Action Performed: Spacebar")
    logger.info("Action Performed: Spacebar")


def response(answer):
    time.sleep(2.5)
    keycompose = str("{"+answer+"}")

    game_window.send_keystrokes(keycompose)
    time.sleep(0.5)
