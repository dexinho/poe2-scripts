import pyautogui


def move_item(x, y):
    pyautogui.moveTo(x, y, 0.1)
    pyautogui.keyDown("ctrl")
    pyautogui.click()
    pyautogui.keyUp("ctrl")
