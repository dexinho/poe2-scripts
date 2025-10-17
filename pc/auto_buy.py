from utility.config import REGIONS, FOLDER_PATHS, IMAGE_NAMES, HIDEOUT_OWNERS
from utility.locate_image import locate_image
from utility.focus_game import focus_game
from utility.enter_hideout import enter_hideout
from utility.move_item import move_item
import pyautogui

pyautogui.FAILSAFE = False


def join_hideout(owner_name=""):
    pyautogui.sleep(0.1)
    pyautogui.press("enter")
    pyautogui.sleep(0.1)
    pyautogui.typewrite(f"/hideout {owner_name}")
    pyautogui.sleep(0.1)
    pyautogui.press("enter")


def locate_merchant():
    image_result = locate_image(
        region=REGIONS["merchant"]["logo"],
        folder_path=FOLDER_PATHS["assets"]["images"]["merchant"],
        image_name=IMAGE_NAMES["merchant"]["logo"],
    )
    return image_result["is_found"]


def snipe_item(region, folder, image_name):
    image_result = locate_image(region, folder, image_name)
    if image_result["is_found"]:
        print(image_name)
        move_item(image_result["position"])
    return image_result


def auto_buy():
    focus_game()
    last_join = pyautogui.pyautogui()

    owners = list(HIDEOUT_OWNERS.keys())
    idx = 0
    delay_seconds = 180

    while True:

        if pyautogui.pyautogui() - last_join >= delay_seconds:
            focus_game()
            owner = owners[idx]
            join_hideout(owner)

            idx = (idx + 1) % len(owners)
            last_join = pyautogui.pyautogui()

        is_merchant_found = locate_merchant()
        if not is_merchant_found:
            pyautogui.sleep(0.20)
            continue

        for key in IMAGE_NAMES["items"]:
            image_result = snipe_item(
                region=REGIONS["merchant"]["area"],
                folder_path=FOLDER_PATHS["assets"]["images"]["items"],
                image_name=IMAGE_NAMES["items"][key],
            )
            if image_result["is_found"]:
                break

        enter_hideout()
        focus_game()


auto_buy()
