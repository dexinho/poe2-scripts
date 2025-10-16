import pyautogui
import time
from utility.config import (
    STARTING_POSITIONS,
    PIXEL_SIZES,
    FOLDER_PATHS,
    IMAGE_NAMES,
    REGIONS,
)
from utility.locate_image import locate_image


def from_inventory(
    row_range=(0, 5), col_range=(0, 12), currency_name=None, full_inv_at_once=None
):

    if full_inv_at_once:
        pyautogui.moveTo(STARTING_POSITIONS["inventory"]["first_slot"])
        time.sleep(0.02)
        pyautogui.keyDown("ctrl")
        time.sleep(0.02)
        pyautogui.rightClick()
        time.sleep(0.02)
        pyautogui.keyUp("ctrl")
        time.sleep(0.02)
        return True

    pyautogui.keyDown("ctrl")
    for i in range(col_range[0], col_range[1]):
        for j in range(row_range[0], row_range[1]):
            pyautogui.moveTo(
                STARTING_POSITIONS["inventory"]["first_slot"][0]
                + PIXEL_SIZES["inventory"]["slot"][0] * i,
                STARTING_POSITIONS["inventory"]["first_slot"][1]
                + PIXEL_SIZES["inventory"]["slot"][1] * j,
            )
            time.sleep(0.015)
            pyautogui.click()
            time.sleep(0.015)

    pyautogui.keyUp("ctrl")
    return True


def locate_currency(currency_name):
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["inventory"]["currencies"],
        image_name=IMAGE_NAMES["inventory"]["currencies"][currency_name],
        region=REGIONS["inventory"]["area"],
        confidence=0.85,
    )

    if image_res:
        pyautogui.moveTo(image_res["position"])
        time.sleep(0.02)
        return image_res

    return False


def select_currency(currency_name):
    image_res = locate_currency(currency_name)

    if image_res:
        pyautogui.rightClick()
        time.sleep(0.02)

        return image_res

    return False
