import pyautogui
import time


def move_item(pos):
    pyautogui.moveTo(pos)
    time.sleep(0.05)

    pyautogui.keyDown("ctrl")
    time.sleep(0.05)

    pyautogui.click()
    time.sleep(0.05)

    pyautogui.keyUp("ctrl")
    time.sleep(0.05)
