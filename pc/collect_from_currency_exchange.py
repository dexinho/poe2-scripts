import pyautogui
from utility.config import (
    STARTING_POSITIONS,
    IMAGE_NAMES,
    FOLDER_PATHS,
    REGIONS,
    PIXEL_SIZES,
)
from utility.locate_image import locate_image
from utility.inventory_management import from_inventory
from utility.open_object import open_stash
from utility.wait_for import wait_for
from utility.focus_game import focus_game

pyautogui.PAUSE = 0


def locate_completed_order():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["ange"][
            "currency_exchange"
        ],
        image_name=IMAGE_NAMES["npcs"]["ange"]["currency_exchange"]["order_completed"],
        region=REGIONS["npcs"]["ange"]["currency_exchange"]["orders"],
    )

    if not image_res["is_found"]:
        print("No more completed orders!")
        exit()

    return image_res["position"]


def from_currency_exchange():
    completed_order_position = locate_completed_order()
    currency_exchange_order_pixel_size = PIXEL_SIZES["currency_exchange"]["order"]
    currency_exchange_slot_pixel_size = PIXEL_SIZES["currency_exchange"]["slot"]
    buying_currency_slot = (
        completed_order_position[0]
        - currency_exchange_order_pixel_size[0] / 2
        + currency_exchange_slot_pixel_size[0] / 2,
        completed_order_position[1] + currency_exchange_order_pixel_size[1] / 2,
    )
    selling_currency_slot = (
        completed_order_position[0]
        + currency_exchange_order_pixel_size[0] / 2
        - currency_exchange_slot_pixel_size[0] / 2,
        completed_order_position[1] + currency_exchange_order_pixel_size[1] / 2,
    )

    pyautogui.sleep(0.01)
    pyautogui.moveTo(buying_currency_slot)
    pyautogui.sleep(0.01)
    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.01)
    pyautogui.rightClick()
    pyautogui.sleep(0.01)
    pyautogui.moveTo(selling_currency_slot)
    pyautogui.sleep(0.01)
    pyautogui.rightClick()
    pyautogui.sleep(0.01)
    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.01)


def open_currency_exchange():
    pyautogui.moveTo(STARTING_POSITIONS["npcs"]["ange"]["position"])
    pyautogui.sleep(0.01)
    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.01)
    pyautogui.click()
    pyautogui.sleep(0.01)
    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.15)

    image_res = locate_image(
        region=REGIONS["npcs"]["ange"]["currency_exchange"]["logo"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["ange"][
            "currency_exchange"
        ],
        image_name=IMAGE_NAMES["npcs"]["ange"]["currency_exchange"]["logo"],
    )

    if image_res["is_found"]:
        return image_res

    return None


def collect_from_currency_exchange():
    focus_game()
    while True:
        wait_for(open_currency_exchange, wait_attempt_threshold=100, delay=0.02)
        from_currency_exchange()
        pyautogui.press("esc")
        pyautogui.sleep(0.01)
        pyautogui.press("esc")
        pyautogui.sleep(0.01)
        wait_for(open_stash, wait_attempt_threshold=100, delay=0.02)
        from_inventory(full_inv_at_once=True)
        pyautogui.press("esc")
        pyautogui.sleep(0.01)


collect_from_currency_exchange()
