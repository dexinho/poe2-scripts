import pyautogui

def focus_game():
    pyautogui.moveTo(25, 25)  # focus the game
    pyautogui.rightClick()
    pyautogui.sleep(0.02)
