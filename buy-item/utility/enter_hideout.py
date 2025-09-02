import time
import pyautogui


def enter_hideout():

    time.sleep(0.1)
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.typewrite("/hideout")
    time.sleep(0.5)
    pyautogui.press("enter")
    time.sleep(2)
