import pyautogui
from utility.config import (
    IMAGE_NAMES,
    FOLDER_PATHS,
    REGIONS,
    STARTING_POSITIONS,
    PIXEL_SIZES,
    GENERATE_GOLD_DATA,
)
from utility.locate_image import locate_image
from utility.move_item import move_item
from utility.focus_game import focus_game
from utility.open_object import open_npc_shop
from utility.wait_for import wait_for
from utility.join_hideout import join_hideout
from utility.inventory_management import (
    from_inventory,
    locate_currency_in_inventory,
)
from utility.stash_management import open_stash, locate_currency_in_currency_tab
from utility.main import start_poe2, character_active
from utility.errors import PoeCharacterNotActive, PoeCharacterBugged

pyautogui.PAUSE = 0
action_delay = GENERATE_GOLD_DATA["action_delay"]


def select_omen_of_bartering():
    wait_for(open_stash, wait_attempt_threshold=25, delay=0.02)
    wait_for(
        locate_currency_in_currency_tab,
        "omen of bartering",
        wait_attempt_threshold=25,
        delay=0.02,
    )
    move_item(pyautogui.position())
    pyautogui.sleep(0.1)
    wait_for(
        locate_currency_in_inventory,
        "omen of bartering",
        wait_attempt_threshold=25,
        delay=0.02,
    )
    pyautogui.rightClick()
    pyautogui.sleep(0.01)
    pyautogui.press("esc")
    pyautogui.sleep(action_delay)


def buy_from_gwennen():
    wait_for(
        open_npc_shop,
        {"name": "gwennen", "option": "deal"},
        wait_attempt_threshold=10,
        delay=0.01,
    )

    # in case of deal window still being open
    if is_gwennen_deal_window_open():
        pyautogui.moveTo(450, 750)
        pyautogui.sleep(action_delay)
        pyautogui.click()
        pyautogui.sleep(action_delay)

    pyautogui.hotkey("ctrl", "f")
    pyautogui.sleep(action_delay)
    pyautogui.typewrite(".")
    pyautogui.sleep(action_delay)
    pyautogui.press("enter")

    if (
        GENERATE_GOLD_DATA["total_items_bought"]
        % GENERATE_GOLD_DATA["refresh_shop_trehshold"]
        == 0
        and GENERATE_GOLD_DATA["total_items_bought"] != 0
    ):
        # in case of leftover item being selected, it will take the selected item

        wait_for(refesh_gwennen_shop, wait_attempt_threshold=25, delay=0.02)

    items_bought_from_gwennen_res = buy_items_from_gwennen(
        GENERATE_GOLD_DATA["item_purchase_quantity"]
    )
    GENERATE_GOLD_DATA["total_items_bought"] += GENERATE_GOLD_DATA[
        "item_purchase_quantity"
    ]

    pyautogui.press("esc")
    pyautogui.sleep(action_delay)

    return items_bought_from_gwennen_res


def handle_purchase_window():

    print("waiting for purchase window...")
    image_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["purchase_window"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["purchase_window"],
        constant_focus=False,
    )

    if image_res:
        pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["buy_button"])
        pyautogui.sleep(0.12)
        pyautogui.click()

    return image_res


def handle_deal_window():
    print("waiting for deal window...")
    image_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["deal_window"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["deal_window"],
        constant_focus=False,
    )

    if image_res:
        pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["take_item_button"])
        pyautogui.sleep(0.12)
        pyautogui.click()

    return image_res


def handle_prepare_item_for_purchase():
    image_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["area"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["item_highlight"],
        constant_focus=False,
    )

    if image_res:
        move_item(image_res["position"])
        print("clicked on item to buy....")

    return image_res


def buy_items_from_gwennen(item_purchase_quantity):
    print(f"Buying items from Gwennen...")
    starting_slot_position = STARTING_POSITIONS["npcs"]["gwennen"]["area"]["first_slot"]

    image_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["area"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["item_highlight"],
        constant_focus=False,
    )

    if not image_res:
        return {"items_bought_quantity": 0}

    for i in range(0, 5, 1):
        for j in range(1, 8, 2):
            pyautogui.moveTo(
                starting_slot_position[0] + PIXEL_SIZES["inventory"]["slot"][0] * i,
                starting_slot_position[1] + PIXEL_SIZES["inventory"]["slot"][1] * j,
            )
            pyautogui.sleep(0.01)
            pyautogui.click()
            pyautogui.sleep(0.01)
            pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["buy_button"])
            pyautogui.sleep(0.01)
            pyautogui.click()
            pyautogui.sleep(0.01)
            pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["take_item_button"])
            pyautogui.sleep(0.01)
            pyautogui.click()
            pyautogui.sleep(0.01)

    return {"items_bought_quantity": item_purchase_quantity}


# def buy_items_from_gwennen(item_purchase_quantity):
#     print(f"Buying items from Gwennen...")
#     for i in range(item_purchase_quantity):

#         image_res = locate_image(
#             region=REGIONS["npcs"]["gwennen"]["deal"]["area"],
#             folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
#             image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["item_highlight"],
#             constant_focus=False,
#         )

#         if not image_res:
#             break

#         pyautogui.sleep(0.04)
#         move_item(image_res["position"])
#         print("found item", i)
#         pyautogui.sleep(action_delay)
#         pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["buy_button"])
#         pyautogui.sleep(0.04)
#         pyautogui.click()
#         pyautogui.sleep(0.04)
#         pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["take_item_button"])
#         pyautogui.sleep(0.04)
#         pyautogui.click()
#         pyautogui.sleep(action_delay)
#         # wait_for(
#         #     handle_prepare_item_for_purchase,
#         #     wait_attempt_threshold=25,
#         #     delay=0.001,
#         # )
#         # wait_for(
#         #     handle_purchase_window,
#         #     wait_attempt_threshold=25,
#         #     delay=0.001,
#         # )
#         # wait_for(
#         #     handle_deal_window,
#         #     wait_attempt_threshold=25,
#         #     delay=0.001,
#         # )


def use_currency(currency_name):
    wait_for(
        locate_currency_in_currency_tab,
        currency_name,
        wait_attempt_threshold=25,
        delay=0.02,
    )

    pyautogui.rightClick()
    pyautogui.sleep(action_delay)
    pyautogui.keyDown("shift")
    pyautogui.sleep(action_delay)
    for row_idx in range(1, 4, 2):
        for column_idx in range(12):
            x = (
                STARTING_POSITIONS["inventory"]["first_slot"][0]
                + PIXEL_SIZES["inventory"]["slot"][0] * column_idx
            )
            y = (
                STARTING_POSITIONS["inventory"]["first_slot"][1]
                + PIXEL_SIZES["inventory"]["slot"][1] * row_idx
            )

            pyautogui.moveTo(x, y)
            pyautogui.sleep(action_delay)
            pyautogui.click()
            pyautogui.sleep(action_delay)

    pyautogui.keyUp("shift")
    pyautogui.sleep(action_delay)


def refesh_gwennen_shop():
    refresh_shop_button_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["refresh_shop_button"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["refresh_shop_button"],
        confidence=0.85,
    )

    if refresh_shop_button_res:
        pyautogui.moveTo(refresh_shop_button_res["position"])
        pyautogui.sleep(action_delay)
        pyautogui.click()
        pyautogui.sleep(0.1)

    return refresh_shop_button_res


def is_gwennen_deal_window_open():
    image_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["item_craft_window"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["item_craft_window"],
        confidence=0.90,
    )

    return image_res


def modify_gwennen_items(modifier_currency):
    wait_for(open_stash, wait_attempt_threshold=25, delay=0.01)
    print(f"Modifying Gwennen's items...")
    use_currency(modifier_currency)
    pyautogui.press("esc")
    pyautogui.sleep(action_delay)


def handle_hideout_change(change_hideout=None):

    if change_hideout or (
        GENERATE_GOLD_DATA["total_items_bought"]
        % GENERATE_GOLD_DATA["hideout_refresh_treshold"]
        == 0
        and GENERATE_GOLD_DATA["total_items_bought"] != 0
    ):
        print(f"Changing hideout...")
        join_hideout(GENERATE_GOLD_DATA["hideout_owner_name"])
        join_hideout(GENERATE_GOLD_DATA["hideout_owner_name_backup"])
        pyautogui.sleep(2.5)
        wait_for(character_active, wait_attempt_threshold=250, delay=0.1)
        join_hideout()
        pyautogui.sleep(2.5)
        wait_for(character_active, wait_attempt_threshold=100, delay=0.1)
        GENERATE_GOLD_DATA["is_hideout_changed"] = True


def return_omen_of_bartering_to_stash():
    wait_for(open_stash, wait_attempt_threshold=25, delay=0.02)
    from_inventory(currency_name="omen of bartering")
    pyautogui.press("esc")
    pyautogui.sleep(action_delay)


def sell_gwennen_items():
    print(f"Selling Gwennen's items...")

    wait_for(
        open_npc_shop,
        {"name": "gwennen", "option": "deal"},
        wait_attempt_threshold=10,
        delay=0.02,
    )
    from_inventory(row_range=(1, 2), col_range=(0, 12))
    from_inventory(row_range=(3, 4), col_range=(0, 12))
    pyautogui.press("esc")
    pyautogui.sleep(action_delay)


def generate_gold(
    modifier_currency="orb of alchemy",
    use_omen_of_bartering=None,
):

    while True:
        try:

            if not character_active():
                raise PoeCharacterNotActive("Character not active!")

            if not GENERATE_GOLD_DATA["is_game_focused"]:
                focus_game()
                pyautogui.sleep(1)
                GENERATE_GOLD_DATA["is_game_focused"] = True

            handle_hideout_change()

            if use_omen_of_bartering:
                select_omen_of_bartering()

            # buying_from_gwennen_res = buy_from_gwennen()
            # items_bought_quantity = buying_from_gwennen_res["items_bought_quantity"]
            # if items_bought_quantity == 0:
            #     continue

            buy_from_gwennen()
            modify_gwennen_items(modifier_currency)
            sell_gwennen_items()
            if use_omen_of_bartering:
                return_omen_of_bartering_to_stash()

        except pyautogui.FailSafeException:
            exit()

        except PoeCharacterBugged:
            handle_hideout_change(change_hideout=True)

        except PoeCharacterNotActive:
            start_poe2()
            join_hideout()
            continue


generate_gold(modifier_currency="orb of alchemy", use_omen_of_bartering=None)
