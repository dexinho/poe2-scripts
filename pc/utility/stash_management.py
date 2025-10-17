import pyautogui

from utility.config import (
    FOLDER_PATHS,
    IMAGE_NAMES,
    REGIONS,
    PIXEL_SIZES,
    STARTING_POSITIONS,
)
from utility.locate_image import locate_image
from utility.move_item import move_item


def locate_currency_from_currency_tab(currency_name):
    pyautogui.hotkey("ctrl", "f")
    pyautogui.sleep(0.02)
    pyautogui.typewrite(f"^{currency_name}$")
    pyautogui.sleep(0.02)
    
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["currency"],
        image_name=IMAGE_NAMES["stash"]["tabs"]["currency"]["highlight"],
        region=REGIONS["stash"]["tabs"]["currency"]["area"],
        confidence=0.95,
    )

    if image_res["is_found"]:
        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.02)
        return image_res

    return None


def open_stash_tab(tab_slot_position):
    x = STARTING_POSITIONS["stash"]["tabs"]["first_slot"][0]
    y = (
        STARTING_POSITIONS["stash"]["tabs"]["first_slot"][1]
        + PIXEL_SIZES["stash"]["tab"][1] * tab_slot_position
    )
    pyautogui.moveTo(x, y)
    pyautogui.sleep(0.1)
    pyautogui.click()
    pyautogui.sleep(1)


def from_currency_tab(currency_name):
    currency_position = locate_currency_from_currency_tab(currency_name)

    move_item(currency_position)
