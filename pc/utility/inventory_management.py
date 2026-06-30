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
    row_range=(0, 5),
    col_range=(0, 12),
    step=1,
    currency_name=None,
    full_inv_at_once=None,
):
    print(f"Moving from inventory...")
    if currency_name:
        locating_res = locate_currency_in_inventory(currency_name=currency_name)
        pyautogui.sleep(0.015)
        pyautogui.keyDown("ctrl")
        pyautogui.sleep(0.015)
        pyautogui.moveTo(locating_res["position"])
        pyautogui.sleep(0.015)
        pyautogui.click()
        pyautogui.sleep(0.015)
        pyautogui.keyUp("ctrl")
        pyautogui.sleep(0.015)

        return locating_res

    if full_inv_at_once:
        pyautogui.moveTo(STARTING_POSITIONS["inventory"]["first_slot"])
        pyautogui.sleep(0.01)
        pyautogui.keyDown("ctrl")
        pyautogui.sleep(0.01)
        pyautogui.rightClick()
        pyautogui.sleep(0.01)
        pyautogui.rightClick()
        pyautogui.sleep(0.01)
        pyautogui.keyUp("ctrl")
        pyautogui.sleep(0.01)
        return True

    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.05)
    for i in range(col_range[0], col_range[1], step):
        for j in range(row_range[0], row_range[1], step):
            pyautogui.moveTo(
                STARTING_POSITIONS["inventory"]["first_slot"][0]
                + PIXEL_SIZES["inventory"]["slot"][0] * i,
                STARTING_POSITIONS["inventory"]["first_slot"][1]
                + PIXEL_SIZES["inventory"]["slot"][1] * j,
            )
            pyautogui.sleep(0.02)
            pyautogui.click()
            pyautogui.sleep(0.02)

    pyautogui.keyUp("ctrl")
    return True


def select_currency_in_inventory(currency_name):
    image_res = locate_currency_in_inventory(currency_name)

    if image_res:
        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.1)
        pyautogui.rightClick()
        pyautogui.sleep(0.1)

    return image_res


def locate_currency_in_inventory(currency_name):
    # print(f"Locating {currency_name} in inventory...")
    fixed_currency_name = currency_name.replace(" ", "_")
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["inventory"]["currencies"],
        image_name=IMAGE_NAMES["inventory"]["currencies"][fixed_currency_name],
        region=REGIONS["inventory"]["area"],
        confidence=0.80,
    )

    return image_res
