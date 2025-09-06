from utility.config import REGIONS, FOLDER_PATHS, FILE_NAMES
from utility.find_image import find_image
from utility.focus_game import focus_game
from utility.enter_hideout import enter_hideout
from utility.move_item import move_item
import pyautogui
import time  # <-- added

pyautogui.PAUSE = 0

def find_merchant():
    image_result = find_image(
        region=REGIONS["merchant"]["logo"],
        folder=FOLDER_PATHS["assets"]["images"]["merchant"],
        image_name=FILE_NAMES["assets"]["images"]["merchant"]["logo"],
    )

    return image_result["is_found"]


def snipe_item(region, folder, image_name):
    image_result = find_image(region, folder, image_name)

    if image_result["is_found"]:
        print(image_name)
        move_item(x=image_result["position"]["x"], y=image_result["position"]["y"])

    return image_result


def auto_buy():
    while True:
        is_merchant_found = find_merchant()
        if not is_merchant_found:
            time.sleep(0.05)
            continue

        focus_game()

        for key in FILE_NAMES["assets"]["images"]["items"]:
            image_result = snipe_item(
                region=REGIONS["merchant"]["area"],
                folder=FOLDER_PATHS["assets"]["images"]["items"],
                image_name=FILE_NAMES["assets"]["images"]["items"][key],
            )

            if image_result["is_found"]:
                break

        enter_hideout()
        focus_game()



auto_buy()
