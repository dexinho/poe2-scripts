import pyautogui
from utility.inventory_management import select_currency_in_inventory
from utility.text_from_image import read_text_from_image
from utility.locate_image import locate_image
from utility.wait_for import wait_for
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


def is_final_choice_revealed():
    image_res = locate_image(
        region=REGIONS["crafts"]["desecrate"]["third_choice_bottom_right_corner"],
        folder_path=FOLDER_PATHS["assets"]["images"]["crafts"]["desecrate"],
        image_name=IMAGE_NAMES["crafts"]["desecrate"][
            "third_choice_bottom_right_corner"
        ],
        confidence=0.8,
        constant_focus=False,
    )

    return image_res


def get_desecrate_options():
    options = []

    regions = [
        (380, 600, 500, 50),
        (380, 685, 500, 50),
        (380, 765, 500, 50),
    ]

    for region in regions:
        text = read_text_from_image(region=region)

        if len(text) == 0:
            continue

        options.append(
            {
                "region": region,
                "text": text,
            }
        )

    if len(options) > 0:
        return options

    return None


def reroll_desecrate_mods():
    pyautogui.moveTo(STARTING_POSITIONS["crafts"]["desecrate"]["reroll_button"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.7)


def locate_desecrate_options(desired_desecrate_mod, avoid_desecrate_mod=None):
    desecrate_options = get_desecrate_options()
    desired_desecrate_mod_found = False
    desired_desecrate_mod_position = None
    avoid_desecrate_mod_found = False
    avoid_desecrate_mod_position = None

    if not desecrate_options:
        print("no desecrate options...")
        return None

    print(desecrate_options)

    for desecrate_option in desecrate_options:
        match_desired_desecrate_mod = False
        match_avoid_desecrate_mod = False
        match_desired_desecrate_mod = re.search(
            desired_desecrate_mod, desecrate_option["text"], re.IGNORECASE
        )

        if avoid_desecrate_mod:
            match_avoid_desecrate_mod = re.search(
                avoid_desecrate_mod, desecrate_option["text"], re.IGNORECASE
            )

        region = desecrate_option["region"]
        x, y, width, height = region

        center_x = x + width // 2
        center_y = y + height // 2

        if match_desired_desecrate_mod:

            desired_desecrate_mod_found = True
            desired_desecrate_mod_position = (center_x, center_y)

        elif match_avoid_desecrate_mod:

            avoid_desecrate_mod_found = True
            avoid_desecrate_mod_position = (center_x, center_y)

    return {
        "desired_desecrate_mod": {
            "found": desired_desecrate_mod_found,
            "position": desired_desecrate_mod_position,
        },
        "avoid_desecrate_mod": {
            "found": avoid_desecrate_mod_found,
            "position": avoid_desecrate_mod_position,
        },
    }


def to_well_of_souls(desecrated_item_position=None):
    if desecrated_item_position:
        pyautogui.moveTo(desecrated_item_position)
        pyautogui.sleep(0.05)

    with pyautogui.hold("ctrl"):
        pyautogui.sleep(0.15)
        pyautogui.click()
        pyautogui.sleep(0.05)

    return True


def from_well_of_souls(
    desired_desecrate_mod_position=None, avoid_desecrate_mod_position=None
):
    x, y, width, height = REGIONS["crafts"]["desecrate"]["options_area"]
    third = height // 3

    print(avoid_desecrate_mod_position)
    if desired_desecrate_mod_position:
        pyautogui.moveTo(desired_desecrate_mod_position)
        pyautogui.sleep(0.2)

    elif avoid_desecrate_mod_position:
        print("ulaziiiiiiiii")

        avoid_y = avoid_desecrate_mod_position[1]
        avoid_third = min((avoid_y - y) // third, 2)

        valid_thirds = [0, 2]

        if avoid_third in valid_thirds:
            valid_thirds.remove(avoid_third)

        roll = random.choice(valid_thirds)

        pyautogui.moveTo(
            random.randint(x, x + width - 1),
            random.randint(
                y + roll * third,
                y + (roll + 1) * third - 1,
            ),
        )
        pyautogui.sleep(0.2)

    else:

        roll = random.choice((0, 2))

        pyautogui.moveTo(
            random.randint(x, x + width - 1),
            random.randint(
                y + roll * third,
                y + (roll + 1) * third - 1,
            ),
        )

    pyautogui.sleep(0.05)
    pyautogui.click()
    pyautogui.sleep(0.03)
    pyautogui.moveTo(STARTING_POSITIONS["crafts"]["desecrate"]["confirm_button"])
    pyautogui.sleep(0.04)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.moveTo(STARTING_POSITIONS["crafts"]["desecrate"]["item_slot"])
    pyautogui.sleep(0.1)
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
    item_to_crafts_width=1,
    item_to_crafts_height=1,
    reroll_desecrate_mods_available=True,
    avoid_desecrate_mod=None,
):
    focus_game(mouse_pos=(633, 310))
    desecrate_attempts_tried = 0
    items_desecrated = 0
    for i in range(0, 12, item_to_crafts_width):
        for j in range(0, 5, item_to_crafts_height):
            if items_desecrated >= max_items_to_desecrate:
                print("item crafts limit reached...")
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

                pyautogui.moveTo(
                    STARTING_POSITIONS["crafts"]["desecrate"]["reveal_button"]
                )
                pyautogui.sleep(0.04)
                pyautogui.click()
                pyautogui.sleep(0.8)
                remove_sold_item_notification_popup()

                desecrate_attempts_tried += 1

                desecrate_option_location = locate_desecrate_options(
                    desired_desecrate_mod=desired_desecrate_mod,
                    avoid_desecrate_mod=avoid_desecrate_mod,
                )

                if desecrate_option_location["desired_desecrate_mod"]["found"]:
                    items_desecrated += 1
                    from_well_of_souls(
                        desired_desecrate_mod_position=desecrate_option_location[
                            "desired_desecrate_mod"
                        ]["position"],
                    )
                    break

                if not reroll_desecrate_mods_available:
                    from_well_of_souls()
                    continue

                reroll_desecrate_mods()
                remove_sold_item_notification_popup()
                desecrate_option_location = locate_desecrate_options(
                    desired_desecrate_mod=desired_desecrate_mod,
                    avoid_desecrate_mod=avoid_desecrate_mod,
                )

                if desecrate_option_location["desired_desecrate_mod"]["found"]:
                    items_desecrated += 1
                    from_well_of_souls(
                        desired_desecrate_mod_position=desecrate_option_location[
                            "desired_desecrate_mod"
                        ]["position"]
                    )
                    break

                from_well_of_souls(
                    avoid_desecrate_mod_position=desecrate_option_location[
                        "avoid_desecrate_mod"
                    ]["position"]
                )


# def remove_desecrate_tooltip_popup():
#     tooltip_res = locate_image(
#         folder_path=FOLDER_PATHS["assets"]["images"]["crafts"]["desecrate"],
#         image_name=IMAGE_NAMES["crafts"]["desecrate"][
#             "desecrated_modifiers_tooltip_popup"
#         ],
#         region=REGIONS["crafts"]["desecrate"]["desecrated_modifiers_tooltip_popup"],
#         confidence=0.8,
#     )

#     pyautogui.moveTo(tooltip_res["position"])


def remove_sold_item_notification_popup():
    tooltip_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["ange"]["merchant"],
        image_name=IMAGE_NAMES["npcs"]["ange"]["merchant"][
            "item_sold_notification_x_button"
        ],
        region=REGIONS["npcs"]["ange"]["merchant"]["item_sold_notification_x_button"],
        confidence=0.8,
    )

    if tooltip_res:
        pyautogui.moveTo(tooltip_res["position"])
        pyautogui.sleep(0.05)
        pyautogui.click()
        pyautogui.sleep(0.05)

        return True

    return None

max_items_to_desecrate = 3
max_desecrate_attempts = 90
# avoid_desecrate_mod = "increased global armour.*shield"
desired_desecrate_mod = "(4[7-9]|50).*spirit"
# desired_desecrate_mod = "(2[7-9]|30)%.*spell damage"
# desired_desecrate_mod = "3.*proj.*lls"
# desired_desecrate_mod = "2[5-8].*cast speed"
# desired_desecrate_mod = "18([0-9]).*max.*mana|[7-8]%.*max.*mana"
# desired_desecrate_mod = "18([0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit"
# currencies_to_use = ["perfect_essence_of_the_infinite", "preserved_collarbone"]
runic_alloy = "runic_alloy"
perfect_essence_of_enhancment = "perfect_essence_of_enhancment"
preserved_collarbone = "preserved_collarbone"
currencies_to_use = [runic_alloy, preserved_collarbone]
desecrate(
    desired_desecrate_mod=desired_desecrate_mod,
    # avoid_desecrate_mod=avoid_desecrate_mod,
    currencies_to_use=currencies_to_use,
    max_items_to_desecrate=max_items_to_desecrate,
    max_desecrate_attempts=max_desecrate_attempts,
    reroll_desecrate_mods_available=True,
)
