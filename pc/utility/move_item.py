import pyautogui


def move_item(position):
    pyautogui.moveTo(position)
    pyautogui.sleep(0.05)

    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.05)

    pyautogui.click()
    pyautogui.sleep(0.05)

    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.05)
