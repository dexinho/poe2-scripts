from utility.config import REGIONS, FOLDER_PATHS, IMAGE_NAMES, HIDEOUT_OWNERS
from utility.locate_image import locate_image
from utility.focus_game import focus_game
from utility.join_hideout import join_hideout
from utility.move_item import move_item
from utility.main import start_poe2, character_active
from utility.main import wait_for
from utility.errors import PoeCharacterNotActive
import pyautogui
import time

# pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0


def handle_hideout_change(hideout_owner_name=""):

    print(f"Changing hideout...")
    join_hideout(hideout_owner_name)
    pyautogui.sleep(2.5)
    wait_for(character_active, wait_attempt_threshold=250, delay=0.1)


def locate_merchant_logo():
    image_result = locate_image(
        region=REGIONS["npcs"]["ange"]["merchant"]["logo_buying"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["ange"]["merchant"],
        image_name=IMAGE_NAMES["npcs"]["ange"]["merchant"]["logo_buying"],
    )
    return image_result["is_found"]


def snipe_item(region, folder_path, image_name):

    image_result = locate_image(
        region=region, folder_path=folder_path, image_name=image_name
    )
    if image_result["is_found"]:
        print(image_name, "found...")
        move_item(image_result["position"])
        pyautogui.sleep(0.5)
        move_item(image_result["position"])
        pyautogui.sleep(0.5)
        move_item(image_result["position"])

    return image_result


def find_highlighted_item():
    print("finding highlighted item...")

    for item_highlight in IMAGE_NAMES["npcs"]["ange"]["merchant"]:

        if not item_highlight.startswith("item_highlight"):
            continue

        image_result = snipe_item(
            region=REGIONS["npcs"]["ange"]["merchant"]["area_buying"],
            folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["ange"]["merchant"],
            image_name=IMAGE_NAMES["npcs"]["ange"]["merchant"][item_highlight],
        )
        if image_result["is_found"]:
            return True

    return None


def auto_buy():
    focus_game()
    last_join = time.time()

    hideout_owner_names = list(HIDEOUT_OWNERS.keys())
    idx = 0
    max_items_to_buy = 40
    delay_seconds = 120
    items_bought = 0

    while True:
        try:
            if items_bought >= max_items_to_buy:
                print(f"Purchased {items_bought} items. Ending script.")
                exit()

            if time.time() - last_join >= delay_seconds:
                focus_game()
                hideout_owner_name = hideout_owner_names[idx]
                handle_hideout_change(hideout_owner_name)

                idx = (idx + 1) % len(hideout_owner_names)
                last_join = time.time()

            is_merchant_found = locate_merchant_logo()
            if not is_merchant_found:
                pyautogui.sleep(0.2)
                continue

            print("found merchant logo...")
            print(f"items bought {items_bought}")

            highlighted_item_res = find_highlighted_item()
            if highlighted_item_res:
                items_bought = items_bought + 1
                handle_hideout_change()

        except pyautogui.FailSafeException:
            exit()

        except PoeCharacterNotActive:
            start_poe2()
            continue


auto_buy()
