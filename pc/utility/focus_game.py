import pyautogui


def focus_game(mouse_pos=(25, 25)):

    pyautogui.moveTo(mouse_pos)  # focus the game
    pyautogui.rightClick()
    pyautogui.sleep(0.25)
