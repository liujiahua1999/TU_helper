from pywinauto.application import Application
from pywinauto.mouse import click
import json, time, logging
from click import click,moveover

with open('PATH.json', 'r') as config_file:
    config = json.load(config_file)


debug_path = config["debug_path"]
alert_sound_path = config["alert_sound_path"] 
folder_path = config["folder_path"]  
template_path = config["template_path"] 


logging.basicConfig(filename="Keypress.log", format='%(asctime)s %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


app = Application(backend="win32").connect(path=r"E:\SteamLibrary\steamapps\common\Tower Unite\Tower\Binaries\Win64")
game_window = app['Tower Unite  ']

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
    print("Initialization Complete")


def space():
    game_window.send_keystrokes("{SPACE}")
    time.sleep(5.5)
    print("Keypress: Spacebar")
    logger.info("Keypress: Spacebar")


def response(answer):
    time.sleep(2.5)
    keycompose = str("{"+answer+"}")

    game_window.send_keystrokes(keycompose)
    time.sleep(0.5)
    print("Answer: " + str(answer))
    logger.info("Answer: "+ str(answer))


def reconnect_tp():
    game_window.send_keystrokes("{SPACE}")
    time.sleep(1.5)
    game_window.send_keystrokes("{M}")
    time.sleep(1.5)
    moveover(65,240)
    time.sleep(0.3)
    click(65,240)
    time.sleep(0.3)
    game_window.send_keystrokes("{ESC}")
    time.sleep(0.3)
    game_window.send_keystrokes("{ESC}")




def movetomachine():

    try:
        game_window.send_keystrokes("{W down}")
        time.sleep(2.5)
        game_window.send_keystrokes("{W up}")
    except:
        pass
    time.sleep(0.5)
    try:
        game_window.send_keystrokes("{A down}")
        time.sleep(0.4)
        game_window.send_keystrokes("{A up}")
    except:
        pass
    time.sleep(0.5)
    try:
        game_window.send_keystrokes("{W down}")
        time.sleep(3.8)
        game_window.send_keystrokes("{W up}")
    except:
        pass
    time.sleep(0.5)
    try:
        game_window.send_keystrokes("{A down}")
        time.sleep(1.2)
        game_window.send_keystrokes("{A up}")
    except:
        pass
    time.sleep(0.5)
    try:
        game_window.send_keystrokes("{W down}")
        time.sleep(1.4)
        game_window.send_keystrokes("{W up}")
    except:
        pass

    game_window.send_keystrokes("{E}")