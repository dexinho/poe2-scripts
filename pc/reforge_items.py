import pyautogui
import random
from utility.inventory_management import from_inventory
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
from utility.stash_management import open_stash, select_stash_tab

pyautogui.PAUSE = 0


def take_currency(quantity):
    pyautogui.moveTo(
        STARTING_POSITIONS["stash"]["tabs"]["currency"]["extra_slots_first_slot"]
    )
    pyautogui.sleep(0.05)

    for i in range(0, quantity):
        with pyautogui.hold("ctrl"):
            pyautogui.sleep(0.05)
            pyautogui.click()
            pyautogui.sleep(0.05)

    return True


def open_reforging_bench():
    pyautogui.moveTo(STARTING_POSITIONS["crafts"]["reforging_bench"]["position"])
    pyautogui.sleep(0.05)
    pyautogui.click()
    pyautogui.sleep(0.5)

    logo_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["crafts"]["reforging_bench"],
        image_name=IMAGE_NAMES["crafts"]["reforging_bench"]["logo"],
        region=REGIONS["crafts"]["reforging_bench"]["logo"],
    )

    if not logo_res:
        print("reforging bench logo not found...")

    return logo_res


def randomize_click_postiion(position, offset_x, offset_y):
    position_x = position[0]
    position_y = position[1]

    pyautogui.moveTo(
        position_x + random.randint(-offset_x, offset_x),
        position_y + random.randint(-offset_y, offset_y),
    )
    pyautogui.sleep(0.02)
    pyautogui.click()


def click_reforge_button():
    reforge_button_position = STARTING_POSITIONS["crafts"]["reforging_bench"][
        "reforge_button"
    ]

    offset_x = 50
    offset_y = 10
    randomize_click_postiion(
        position=reforge_button_position, offset_x=offset_x, offset_y=offset_y
    )
    pyautogui.sleep(0.7)


def remove_reforged_item():
    reforged_item_position = STARTING_POSITIONS["crafts"]["reforging_bench"][
        "reforging_result_slot"
    ]

    offset_x = 30
    offset_y = 50

    randomize_click_postiion(
        position=reforged_item_position, offset_x=offset_x, offset_y=offset_y
    )
    pyautogui.sleep(0.05)


def start_reforging(attempts):
    for _ in range(0, attempts):
        click_reforge_button()
        remove_reforged_item()

    return True


def exit_stash():
    pyautogui.moveTo(STARTING_POSITIONS["stash"]["exit_button"])
    pyautogui.sleep(0.05)
    pyautogui.click()
    pyautogui.sleep(0.25)

    return True


def exit_reforging_bench():
    pyautogui.moveTo(STARTING_POSITIONS["crafts"]["reforging_bench"]["exit_button"])
    pyautogui.sleep(0.05)
    pyautogui.click()
    pyautogui.sleep(0.5)

    return True


def reforge_items():
    quantity = 45
    reforging_bench_items_input_limit = 200
    focus_game()

    while True:

        wait_for(open_stash, delay=0.1)
        select_stash_tab(tab_position=0, slow_load=False)
        from_inventory(row_range=(0, 5), col_range=(0, 12))
        take_currency(quantity)
        exit_stash()
        wait_for(open_reforging_bench)

        reforging_bench_slot_limit = 3
        reforging_bench_items_input = 0
        reforging_bench_attempts = 10
        for i in range(0, 9):
            for j in range(0, 5):
                with pyautogui.hold("ctrl"):
                    pyautogui.moveTo(
                        STARTING_POSITIONS["inventory"]["first_slot"][0]
                        + PIXEL_SIZES["inventory"]["slot"][0] * i,
                        STARTING_POSITIONS["inventory"]["first_slot"][1]
                        + PIXEL_SIZES["inventory"]["slot"][1] * j,
                    )
                    pyautogui.sleep(0.02)
                    pyautogui.click()
                    pyautogui.sleep(0.02)

                    reforging_bench_items_input += 1

                    if reforging_bench_items_input >= reforging_bench_items_input_limit:
                        print("reforging input limit reached...")
                        return True

                    if reforging_bench_items_input % reforging_bench_slot_limit == 0:
                        start_reforging(attempts=reforging_bench_attempts)

        exit_reforging_bench()


reforge_items()
