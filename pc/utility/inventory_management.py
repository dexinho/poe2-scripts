import pyautogui
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
    print(f"Moving from inventory...")
    if full_inv_at_once:
        pyautogui.moveTo(STARTING_POSITIONS["inventory"]["first_slot"])
        pyautogui.sleep(0.02)
        pyautogui.keyDown("ctrl")
        pyautogui.sleep(0.02)
        pyautogui.rightClick()
        pyautogui.sleep(0.02)
        pyautogui.keyUp("ctrl")
        pyautogui.sleep(0.02)
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
            pyautogui.sleep(0.01)
            pyautogui.click()
            pyautogui.sleep(0.01)

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
        pyautogui.sleep(0.02)
        return image_res

    return None


def select_currency(currency_name):
    image_res = locate_currency(currency_name)

    if image_res:
        pyautogui.rightClick()
        pyautogui.sleep(0.02)

        return image_res

    return None
