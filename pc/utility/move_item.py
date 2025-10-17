import pyautogui


def move_item(pos):
    pyautogui.moveTo(pos)
    pyautogui.sleep(0.02)

    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.02)

    pyautogui.click()
    pyautogui.sleep(0.02)

    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.02)
