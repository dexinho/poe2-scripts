import pyautogui

from utility.radnom_pause import random_pause


def focus_game():
    pyautogui.moveTo(25, 25, 0.05)  # focus the game
    pyautogui.rightClick()
    random_pause(0.02, 0.05)