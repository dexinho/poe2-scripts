import pyautogui

def join_hideout(owner_name=""):
    pyautogui.sleep(0.1)
    pyautogui.press("enter")
    pyautogui.sleep(0.1)
    pyautogui.typewrite(f"/hideout {owner_name}")
    pyautogui.sleep(0.1)
    pyautogui.press("enter")
