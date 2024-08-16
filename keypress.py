from pywinauto.application import Application
import pywinauto.mouse
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


def reconnect_init():
    #Wait 5 Min
    print("Reconnection Started")
    logger.info("Reconnection Started")    
    #time.sleep(300)
    app.top_window().set_focus()
    #Click OK
    moveover(514,435)
    time.sleep(1.5)
    
    pywinauto.mouse.click
    click(514,435)
    time.sleep(3.5)

    #Start Reconnecting
    click(128,100)
    time.sleep(3.5)

    #Choose the Server Rank #2 on the list
    click(734,266)
    #Wait 2 Min
    time.sleep(120)

def reconnect_tp():
    print("Reonnection Teleport to Position Started")
    logger.warning("Reonnection Teleport to Position Started")
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
    print("Move to Machine Started ")
    logger.warning("Move to Machine Started ")
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