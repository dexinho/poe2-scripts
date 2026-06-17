import pyautogui


def move_item(pos):
    pyautogui.moveTo(pos)
    pyautogui.sleep(0.020)

    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.020)

    pyautogui.click()
    pyautogui.sleep(0.020)

    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.020)
