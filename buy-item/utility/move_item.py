import pyautogui
import time


def move_item(x, y):
    pyautogui.moveTo(x, y, duration=0.01)

    pyautogui.keyDown("ctrl")
    time.sleep(0.01)

    pyautogui.click()
    time.sleep(0.01) 

    pyautogui.keyUp("ctrl")
    time.sleep(0.01)
