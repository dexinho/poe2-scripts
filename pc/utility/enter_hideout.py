import time
import pyautogui


def enter_hideout():

    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(0.2)
    pyautogui.typewrite("/hideout")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(2)
