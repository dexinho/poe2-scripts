import pyautogui
import time
from utility.config import REGIONS, FOLDER_PATHS, FILE_NAMES
from utility.find_image import find_image

pyautogui.PAUSE = 0.005


def highlight_items(item_name):
    pyautogui.keyDown("ctrl")
    time.sleep(0.05)
    pyautogui.press("f")
    time.sleep(0.05)
    pyautogui.keyUp("ctrl")
    time.sleep(0.05)
    pyautogui.typewrite(item_name)
    time.sleep(0.05)


def craft_result():
    image_res = find_image(
        region=REGIONS["stash"]["area"],
        folder=FOLDER_PATHS["assets"]["images"]["craft"],
        image_name=FILE_NAMES["assets"]["images"]["craft"]["item_highlight"],
    )

    print(image_res["is_found"])

    if image_res["is_found"]:
        return True


def select_chaos_orb():
    image_res = find_image(
        region=REGIONS["inventory"]["area"],
        folder=FOLDER_PATHS["assets"]["images"]["currency"],
        image_name=FILE_NAMES["assets"]["images"]["currency"]["chaos_orb"],
    )
    if image_res["is_found"]:
        pyautogui.moveTo(image_res["position"]["x"], image_res["position"]["y"])
        time.sleep(0.05)
        pyautogui.rightClick()
        time.sleep(0.05)

        return True

    return False


def chaos_slam():
    chaos_orb_selected = select_chaos_orb()
    if not chaos_orb_selected:
        return

    highlight_items("skills")
    pyautogui.keyDown("shift")
    time.sleep(0.05)
    pyautogui.moveTo(330, 440)
    time.sleep(0.05)
    while True:
        pyautogui.click()
        time.sleep(0.25)
        is_craft_successful = craft_result()

        if is_craft_successful:
            pyautogui.keyUp("shift")
            time.sleep(0.05)
            break


chaos_slam()
