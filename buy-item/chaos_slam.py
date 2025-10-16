import pyautogui
import time
from utility.config import REGIONS, FOLDER_PATHS, IMAGE_NAMES, STARTING_POSITIONS
from utility.inventory_management import select_currency
from utility.locate_image import locate_image

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
    image_res = locate_image(
        region=REGIONS["stash"]["tabs"]["currency"]["middle_extra_slot_area"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["currency"],
        image_name=IMAGE_NAMES["stash"]["tabs"]["currency"]["highlight"],
    )

    print(image_res["is_found"])

    if image_res["is_found"]:
        return True


def select_chaos_orb():
    image_res = select_currency("chaos_orb")

    return image_res


def chaos_slam():
    chaos_orb_selected = select_chaos_orb()
    if not chaos_orb_selected:
        return

    highlight_items("light")
    pyautogui.keyDown("shift")
    time.sleep(0.05)

    while True:
        pyautogui.moveTo(
            STARTING_POSITIONS["stash"]["tabs"]["currency"]["extra_middle_slot"]
        )
        time.sleep(0.02)
        pyautogui.click()
        time.sleep(0.25)
        is_craft_successful = craft_result()

        if is_craft_successful:
            pyautogui.keyUp("shift")
            time.sleep(0.05)
            break


chaos_slam()
