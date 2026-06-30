import pyautogui
from utility.inventory_management import select_currency_in_inventory
from utility.text_from_image import read_text_from_image
from utility.config import (
    REGIONS,
    FOLDER_PATHS,
    IMAGE_NAMES,
    STARTING_POSITIONS,
    PIXEL_SIZES,
)
from utility.focus_game import focus_game
import re
import random

pyautogui.PAUSE = 0


def get_desecrate_options():
    options = []

    regions = [
        {"left": 380, "top": 600, "width": 500, "height": 50},
        {"left": 380, "top": 685, "width": 500, "height": 50},
        {"left": 380, "top": 765, "width": 500, "height": 50},
    ]

    for region in regions:
        text = read_text_from_image(region=region)

        if len(text) == 0:
            continue

        options.append(
            {
                "region": (
                    region["left"],
                    region["top"],
                    region["width"],
                    region["height"],
                ),
                "text": text,
            }
        )

    if len(options) > 0:
        return options

    return None


def reroll_desecrate_mods():
    pyautogui.moveTo(STARTING_POSITIONS["desecrate"]["reroll_button"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.8)


def locate_desecrate_option(desired_desecrate_mod):
    desecrate_options = get_desecrate_options()

    if not desecrate_options:
        print("no desecrate options...")
        return None

    print(desecrate_options)

    for desecrate_option in desecrate_options:
        match = re.search(
            desired_desecrate_mod, desecrate_option["text"], re.IGNORECASE
        )

        if match:
            region = desecrate_option["region"]
            x, y, width, height = region

            center_x = x + width // 2
            center_y = y + height // 2

            return (center_x, center_y)

    return None


def to_well_of_souls(desecrated_item_position):
    with pyautogui.hold("ctrl"):
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(0.05)

    return True


def from_well_of_souls(desecrate_option_position=None):
    if desecrate_option_position:
        pyautogui.moveTo(desecrate_option_position)
        pyautogui.sleep(0.02)
        pyautogui.click()
        pyautogui.sleep(0.02)
    else:
        x, y, width, height = REGIONS["desecrate"]["options_area"]
        pyautogui.moveTo(
            random.randint(x, x + width - 1),
            random.randint(y, y + height - 1),
        )
        pyautogui.sleep(0.02)
        pyautogui.click()
        pyautogui.sleep(0.02)

    pyautogui.moveTo(STARTING_POSITIONS["desecrate"]["confirm_button"])
    pyautogui.sleep(0.04)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.moveTo(STARTING_POSITIONS["desecrate"]["item_slot"])
    pyautogui.sleep(0.05)
    with pyautogui.hold("ctrl"):
        pyautogui.sleep(0.05)
        pyautogui.click()
        pyautogui.sleep(0.05)

    return True


def desecrate(
    desired_desecrate_mod,
    max_items_to_desecrate,
    currencies_to_use,
    max_desecrate_attempts,
    item_to_craft_width=1,
    item_to_craft_height=1,
    reroll_desecrate_mods_available=True,
):
    focus_game()
    desecrate_attempts_tried = 0
    items_desecrated = 0
    for i in range(0, 12, item_to_craft_width):
        for j in range(0, 5, item_to_craft_height):
            if items_desecrated >= max_items_to_desecrate:
                print("item craft limit reached...")
                return True

            desecrated_item_position = (
                STARTING_POSITIONS["inventory"]["first_slot"][0]
                + PIXEL_SIZES["inventory"]["slot"][0] * i,
                STARTING_POSITIONS["inventory"]["first_slot"][1]
                + PIXEL_SIZES["inventory"]["slot"][1] * j,
            )
            while True:
                if desecrate_attempts_tried >= max_desecrate_attempts:
                    print("max desecrate attempts reached...")
                    return True

                for currency_to_use in currencies_to_use:
                    currency_in_inventory_res = select_currency_in_inventory(
                        currency_name=currency_to_use
                    )
                    if not currency_in_inventory_res:
                        print(f"{currency_to_use} not found...")
                        return None

                    pyautogui.moveTo(desecrated_item_position)
                    pyautogui.sleep(0.02)
                    pyautogui.click()
                    pyautogui.sleep(0.02)

                to_well_of_souls(desecrated_item_position=desecrated_item_position)

                pyautogui.moveTo(STARTING_POSITIONS["desecrate"]["reveal_button"])
                pyautogui.sleep(0.04)
                pyautogui.click()
                pyautogui.sleep(0.8)

                desecrate_attempts_tried += 1

                desecrate_option_location = locate_desecrate_option(
                    desired_desecrate_mod=desired_desecrate_mod
                )

                if desecrate_option_location:
                    items_desecrated += 1
                    from_well_of_souls(
                        desecrate_option_position=desecrate_option_location
                    )
                    break

                if not reroll_desecrate_mods_available:
                    from_well_of_souls()
                    continue

                reroll_desecrate_mods()
                desecrate_option_location = locate_desecrate_option(
                    desired_desecrate_mod=desired_desecrate_mod
                )
                if desecrate_option_location:
                    items_desecrated += 1
                    from_well_of_souls(
                        desecrate_option_position=desecrate_option_location
                    )
                    break

                from_well_of_souls()


# desired_desecrate_mod = "(4[7-9]|50).*spirit"
desired_desecrate_mod = "18([0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit"
currencies_to_use = ["runic_alloy", "preserved_collarbone"]
desecrate(
    desired_desecrate_mod=desired_desecrate_mod,
    currencies_to_use=currencies_to_use,
    max_items_to_desecrate=5,
    max_desecrate_attempts=150,
    reroll_desecrate_mods_available=True,
)
