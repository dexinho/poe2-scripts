import pyautogui
from utility.focus_game import focus_game
from utility.config import (
    STARTING_POSITIONS,
    FOLDER_PATHS,
    IMAGE_NAMES,
    REGIONS,
    PIXEL_SIZES,
)
from utility.wait_for import wait_for
from utility.locate_image import locate_image
from utility.stash_management import (
    open_stash,
    select_stash_tab,
    highlight_items,
    locate_currency_in_currency_tab,
)

from utility.inventory_management import locate_currency_in_inventory

pyautogui.PAUSE = 0.01


def quick_open_stash_and_npc(npc_name="ange"):
    pyautogui.keyDown("alt")
    pyautogui.sleep(0.02)
    pyautogui.moveTo(STARTING_POSITIONS["stash"]["position"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.moveTo(STARTING_POSITIONS["npcs"][npc_name]["position"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.keyUp("alt")
    pyautogui.sleep(0.2)

    npc_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["ange"][
            "buy_or_sell_items"
        ],
        image_name=IMAGE_NAMES["npcs"]["ange"]["buy_or_sell_items"]["logo"],
        region=REGIONS["npcs"]["ange"]["buy_or_sell_items"]["logo"],
        confidence=0.95,
    )

    print(npc_res)

    if npc_res["is_found"]:
        return True

    return None


def locate_highlighted_item():
    highlight_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["quad"],
        image_name=IMAGE_NAMES["stash"]["tabs"]["quad"]["highlight"],
        region=REGIONS["stash"]["tabs"]["quad"]["area"],
        confidence=0.95,
    )

    return highlight_res


def get_omen_of_bartering(bartering_stack_quantity=11):
    bartering_res = locate_currency_in_currency_tab(currency_name="omen of bartering")

    if bartering_res["is_found"]:
        pyautogui.moveTo(bartering_res["position"])
        pyautogui.sleep(0.02)
        pyautogui.keyDown("ctrl")
        pyautogui.sleep(0.02)
        pyautogui.rightClick()
        pyautogui.sleep(0.02)
        pyautogui.keyUp("ctrl")
        pyautogui.sleep(0.02)
        return True


def select_omen_of_bartering(bartering_stack_quantity=11):
    inventory_slot_first_pos = STARTING_POSITIONS["inventory"]["first_slot"]
    inventory_slot_size = PIXEL_SIZES["inventory"]["slot"]

    omens_selected = 0

    for i in range(12):
        for j in range(5):
            inventory_slot_pos_x = (
                inventory_slot_first_pos[0] + inventory_slot_size[0] * i
            )
            inventory_slot_pos_y = (
                inventory_slot_first_pos[1] + inventory_slot_size[1] * j
            )

            pyautogui.moveTo(inventory_slot_pos_x, inventory_slot_pos_y)
            pyautogui.sleep(0.015)
            pyautogui.rightClick()
            pyautogui.sleep(0.015)

            omens_selected += 1

            if omens_selected == bartering_stack_quantity:
                return {
                    "bartering_position": (
                        inventory_slot_pos_x,
                        inventory_slot_pos_y,
                    )
                }


def from_stash_to_npc():
    quad_col = 23
    quad_row = 24
    quad_slot_first_position = STARTING_POSITIONS["stash"]["tabs"]["quad"]["first_slot"]
    quad_slot_size = PIXEL_SIZES["stash"]["tabs"]["quad"]["slot"]
    npc_area_position = STARTING_POSITIONS["npcs"]["ange"]["buy_and_sell_items"]["area"]

    for row in range(quad_row):
        for col in range(quad_col):
            slot_x = quad_slot_first_position[0] + col * quad_slot_size[0]
            slot_y = quad_slot_first_position[1] + row * quad_slot_size[1]
            region_size_x = 10
            region_size_y = 12
            region = (int(slot_x), int(slot_y), region_size_x, region_size_y)
            image_res = locate_image(
                folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["quad"],
                image_name=IMAGE_NAMES["stash"]["tabs"]["quad"]["highlight"],
                region=region,
                confidence=0.80,
                constant_focus=False,
            )
            print(image_res)

            if not image_res["is_found"]:
                continue

            slot_offset = 5  # we are looking for highlighted outlines and we want to select slot more to the right
            pyautogui.moveTo(slot_x + slot_offset, slot_y + slot_offset)
            pyautogui.sleep(0.03)
            pyautogui.click()
            pyautogui.sleep(0.02)
            pyautogui.moveTo(npc_area_position)
            pyautogui.sleep(0.03)
            pyautogui.click()
            pyautogui.sleep(0.02)

    return True


def omen_of_bartering_to_stash_from_inventory():
    omen_of_bartering_location_res = locate_currency_in_inventory("omen of bartering")
    if omen_of_bartering_location_res["is_found"]:
        pyautogui.moveTo(omen_of_bartering_location_res["position"])
        pyautogui.sleep(0.02)
        pyautogui.keyDown("ctrl")
        pyautogui.sleep(0.02)
        pyautogui.rightClick()
        pyautogui.sleep(0.02)
        pyautogui.keyUp("ctrl")
        pyautogui.sleep(0.02)

    return True


def sell_item_to_npc(item_position):

    pyautogui.moveTo((item_position[0] - 15, item_position[1]))
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.moveTo(STARTING_POSITIONS["npcs"]["ange"]["buy_and_sell_items"]["area"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)


def open_bartering_stash_tab(tab_position):
    select_stash_tab(tab_position=tab_position, slow_load=True)


def sell_quad(quad_tab_positions=[9], use_omen_of_bartering=None):
    bartering_tab_position = 2
    omen_of_bartering_stacks_per_quad = 15
    focus_game()
    for tab_position in quad_tab_positions:
        wait_for(open_stash, delay=0.1)

        if (
            use_omen_of_bartering
        ):  # needs minimum of 120 barterings for the full quad of items
            open_bartering_stash_tab(tab_position=bartering_tab_position)
            omen_of_bartering_to_stash_from_inventory()
            omen_of_bartering_res = get_omen_of_bartering(
                bartering_stack_quantity=omen_of_bartering_stacks_per_quad,
            )

            if not omen_of_bartering_res:
                print("Unable to find omen of bartering...")
                return None

            select_omen_of_bartering_res = select_omen_of_bartering(
                bartering_stack_quantity=omen_of_bartering_stacks_per_quad
            )

        select_stash_tab(tab_position=tab_position, slow_load=False)
        highlight_items()
        wait_for(quick_open_stash_and_npc)
        from_stash_to_npc()

        moving_items = True
        # while moving_items:
        # highlight_res = locate_highlighted_item()
        # if highlight_res["is_found"]:

        #     sell_item_to_npc(item_position=highlight_res["position"])
        # else:
        #     moving_items = False


sell_quad(use_omen_of_bartering=True)

# image_res = locate_image(
#                 folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["quad"],
#                 image_name=IMAGE_NAMES["stash"]["tabs"]["quad"]["highlight"],
#                 region=(15, 124, 100, 100),
#                 confidence=0.80,
#                 constant_focus=False,
#             )

# pyautogui.moveTo(image_res['position'])