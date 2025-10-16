import pyautogui
import time
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
from utility.open_object import open_stash, open_npc_shop
from utility.wait_for import wait_for
from utility.inventory_management import from_inventory, select_currency
from utility.stash_management import locate_currency_tab_currency, open_stash_tab
from utility.poe2_main import start_poe2, click_icon, character_active
from utility.errors import PoeNotActiveError

pyautogui.PAUSE = 0


def handle_omen_of_bartering():
    wait_for(open_stash)

    if is_hideout_changed:
        time.sleep(1)
        is_hideout_changed = False
        open_stash_tab(GENERATE_GOLD_DATA["gold_tab_slot_position"])

    if GENERATE_GOLD_DATA["total_items_bought"] == 0:
        open_stash_tab(GENERATE_GOLD_DATA["gold_tab_slot_position"])

    currency_res = wait_for(locate_currency_tab_currency, "omen of bartering")
    move_item(currency_res["position"])
    select_currency("omen of bartering")
    pyautogui.press("esc")
    time.sleep(0.1)


def buy_from_gwennen():
    wait_for(open_npc_shop, {"name": "gwennen", "option": "deal"})

    if is_gwennen_deal_window_open():
        pyautogui.moveTo(450, 750)
        time.sleep(0.02)
        pyautogui.click()
        time.sleep(0.02)

    pyautogui.hotkey("ctrl", "f")
    time.sleep(0.01)
    pyautogui.typewrite(".")
    time.sleep(0.01)
    pyautogui.press("enter")

    if (
        GENERATE_GOLD_DATA["total_items_bought"]
        % GENERATE_GOLD_DATA["refresh_shop_trehshold"]
        == 0
        and GENERATE_GOLD_DATA["total_items_bought"] != 0
    ):
        # in case of leftover item being selected, it will take the selected item

        refresh_shop()

    buy_items(GENERATE_GOLD_DATA["item_purchase_quantity"])
    GENERATE_GOLD_DATA["total_items_bought"] += GENERATE_GOLD_DATA[
        "item_purchase_quantity"
    ]

    pyautogui.press("esc")
    time.sleep(0.1)


def buy_items(item_purchase_quantity):

    for i in range(item_purchase_quantity):
        image_res = locate_image(
            region=REGIONS["npcs"]["gwennen"]["deal"]["area"],
            folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
            image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["item_highlight"],
        )

        if not image_res["is_found"]:
            break

        move_item(image_res["position"])
        time.sleep(0.02)
        pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["buy_button"])
        time.sleep(0.04)
        pyautogui.click()
        time.sleep(0.04)
        pyautogui.moveTo(STARTING_POSITIONS["npcs"]["gwennen"]["take_item_button"])
        time.sleep(0.04)
        pyautogui.click()
        time.sleep(0.2)


def use_currency(currency_name):
    wait_for(locate_currency_tab_currency, currency_name)

    pyautogui.rightClick()
    time.sleep(0.02)
    pyautogui.keyDown("shift")
    time.sleep(0.02)
    row_index = 2
    for i in range(12):
        x = (
            STARTING_POSITIONS["inventory"]["first_slot"][0]
            + PIXEL_SIZES["inventory"]["slot"][0] * i
        )
        y = (
            STARTING_POSITIONS["inventory"]["first_slot"][1]
            + PIXEL_SIZES["inventory"]["slot"][1] * row_index
        )

        pyautogui.moveTo(x, y)
        time.sleep(0.02)
        pyautogui.click()
        time.sleep(0.02)

    pyautogui.keyUp("shift")
    time.sleep(0.02)


def refresh_shop():
    pyautogui.moveTo(945, 885)
    time.sleep(0.05)
    pyautogui.click()
    time.sleep(0.25)


def is_gwennen_deal_window_open():
    image_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["item_craft_window"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["item_craft_window"],
        confidence=0.90,
    )

    return image_res["is_found"]


def join_hideout(owner_name=""):
    time.sleep(0.15)
    pyautogui.press("enter")
    time.sleep(0.15)
    pyautogui.typewrite(f"/hideout {owner_name}")
    time.sleep(0.15)
    pyautogui.press("enter")


def modify_gwennen_items(modifier_currency):
    wait_for(open_stash)
    use_currency(modifier_currency)
    pyautogui.press("esc")
    time.sleep(0.1)


def handle_hideout_change():
    if (
        GENERATE_GOLD_DATA["total_items_bought"]
        % GENERATE_GOLD_DATA["hideout_refresh_treshold"]
        == 0
        and GENERATE_GOLD_DATA["total_items_bought"] != 0
    ):
        join_hideout(GENERATE_GOLD_DATA["hideout_owner_name"])
        join_hideout(GENERATE_GOLD_DATA["hideout_owner_name_backup"])
        time.sleep(2.5)
        wait_for(character_active)
        join_hideout()
        time.sleep(2.5)
        wait_for(character_active)
        GENERATE_GOLD_DATA["is_hideout_changed"] = True


def sell_gwennen_items():
    wait_for(open_npc_shop, {"name": "gwennen", "option": "deal"})
    from_inventory(row_range=(2, 3), col_range=(0, 12))
    pyautogui.press("esc")
    time.sleep(0.1)


def generate_gold(
    modifier_currency="orb of alchemy",
    use_omen_of_bartering=None,
):

    while True:
        try:
            if not character_active():
                raise PoeNotActiveError("Character not active!")

            if not GENERATE_GOLD_DATA["is_game_focused"]:
                focus_game()
                GENERATE_GOLD_DATA["is_game_focused"] = True

            handle_hideout_change()

            if use_omen_of_bartering:
                handle_omen_of_bartering()

            buy_from_gwennen()
            modify_gwennen_items(modifier_currency)
            sell_gwennen_items()

        except pyautogui.FailSafeException:
            exit()

        except PoeNotActiveError:
            start_poe2()
            continue


generate_gold(modifier_currency="orb of alchemy", use_omen_of_bartering=None)
