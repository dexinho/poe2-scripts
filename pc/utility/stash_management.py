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


def open_stash(is_open_check=True):

    if is_open_check:
        image_res = locate_image(
            region=REGIONS["stash"]["main"]["logo"],
            folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["main"],
            image_name=IMAGE_NAMES["stash"]["main"]["logo"],
        )

        if image_res["is_found"]:
            print(f"Stash opened...")
            return image_res

    print(f"Opening stash...")
    pyautogui.moveTo(STARTING_POSITIONS["stash"]["position"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)

    image_res = locate_image(
        region=REGIONS["stash"]["main"]["logo"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["main"],
        image_name=IMAGE_NAMES["stash"]["main"]["logo"],
    )

    if image_res["is_found"]:
        print(f"Stash opened...")
        return image_res

    return None


def highlight_items(item_name="."):
    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.02)
    pyautogui.press("f")
    pyautogui.sleep(0.02)
    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.02)
    pyautogui.typewrite(item_name)
    pyautogui.sleep(0.05)


def locate_currency_in_currency_tab(currency_name):
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


def select_stash_tab(tab_position, slow_load=True):
    x = STARTING_POSITIONS["stash"]["tabs"]["first_slot"][0]
    y = (
        STARTING_POSITIONS["stash"]["tabs"]["first_slot"][1]
        + PIXEL_SIZES["stash"]["tab"][1] * tab_position
    )
    pyautogui.moveTo(x, y)
    pyautogui.sleep(0.1)
    pyautogui.click()
    if slow_load:
        pyautogui.sleep(1)
    else:
        pyautogui.sleep(0.05)

    return True


def from_currency_tab(currency_name):
    currency_position = locate_currency_in_currency_tab(currency_name)

    move_item(currency_position)
