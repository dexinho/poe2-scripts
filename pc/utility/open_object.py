import pyautogui
import time
from utility.locate_image import locate_image
from utility.config import (
    IMAGE_NAMES,
    FOLDER_PATHS,
    REGIONS,
    STARTING_POSITIONS,
)


def open_stash():
    pyautogui.moveTo(STARTING_POSITIONS["stash"]["position"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    time.sleep(0.02)
    pyautogui.click()
    time.sleep(0.02)
    pyautogui.sleep(0.3)

    image_res = locate_image(
        region=REGIONS["stash"]["main"]["logo"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["main"],
        image_name=IMAGE_NAMES["stash"]["main"]["logo"],
    )

    if image_res["is_found"]:
        return True

    return False


def open_npc_shop(npc):
    npc_name = npc["name"]
    npc_option = npc["option"]
    pyautogui.keyDown("alt")
    time.sleep(0.02)
    pyautogui.moveTo(STARTING_POSITIONS["npcs"][npc_name]["position"])
    pyautogui.click()
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(0.05)
    pyautogui.keyUp("alt")
    time.sleep(0.25)

    image_res = locate_image(
        region=REGIONS["npcs"][npc_name][npc_option]['logo'],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"][npc_name][npc_option],
        image_name=IMAGE_NAMES["npcs"][npc_name][npc_option]['logo'],
    )

    if image_res["is_found"]:
        return True

    # sometimes it struggles to find logo, this is backup that fixes it
    if npc_name == "gwennen":
        pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["refresh_shop_button"])
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(1)
        print("gwennen's shop bugged!")

    return False
