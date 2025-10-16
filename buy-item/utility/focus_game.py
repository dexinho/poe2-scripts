import pyautogui
import time

def focus_game():
    pyautogui.moveTo(25, 25)  # focus the game
    pyautogui.rightClick()
    time.sleep(0.02)
