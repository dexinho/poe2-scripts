import random
import pyautogui
from utility.config import (
    REGIONS,
    FOLDER_PATHS,
    IMAGE_NAMES,
    STARTING_POSITIONS,
    PIXEL_SIZES,
)
from utility.inventory_management import select_currency_in_inventory
from utility.locate_image import locate_image
from utility.stash_management import highlight_items, locate_currency_in_currency_tab
from utility.focus_game import focus_game
from utility.wait_for import wait_for
from utility.move_item import move_item

pyautogui.PAUSE = 0.005


def get_craft_result():
    image_res = locate_image(
        region=REGIONS["stash"]["tabs"]["currency"]["middle_slot_top_left_area"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["currency"],
        image_name=IMAGE_NAMES["stash"]["tabs"]["currency"]["middle_slot_highlight"],
        constant_focus=False,
    )

    return image_res


def select_chaos_orb():
    image_res = select_currency_in_inventory("chaos_orb")

    return image_res


def check_middle_slot():
    image_res = image_res = locate_image(
        region=REGIONS["stash"]["tabs"]["currency"]["middle_slot_area"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["currency"],
        image_name=IMAGE_NAMES["stash"]["tabs"]["currency"]["middle_slot_empty"],
        constant_focus=False,
    )

    return image_res


def craft_items(craft_goal):
    currency_quanitity_used = 0
    items_crafted = 0
    craft_click_delay = 0.02
    random_pause_limit = int(random.uniform(20, 50))
    random_pause_delay = random.uniform(0.1, 0.2)
    currency_quanitity_used_checkpoint = 5
    currency_name = craft_goal["currency_name"]
    highlight_text = craft_goal["highlight_text"]
    crafting_currency_available_quantity = craft_goal[
        "crafting_currency_available_quantity"
    ]
    max_items_to_craft = craft_goal["max_items_to_craft"]
    item_to_craft_width = craft_goal["item_to_craft_width"]
    item_to_craft_height = craft_goal["item_to_craft_height"]

    for i in range(0, 12, item_to_craft_width):
        for j in range(0, 5, item_to_craft_height):
            if items_crafted >= max_items_to_craft:
                print("item craft limit reached...")
                return True

            is_middle_slot_empty = check_middle_slot()

            if not is_middle_slot_empty:
                move_item(
                    position=STARTING_POSITIONS["stash"]["tabs"]["currency"][
                        "middle_slot"
                    ]
                )

            move_item(
                position=(
                    STARTING_POSITIONS["inventory"]["first_slot"][0]
                    + PIXEL_SIZES["inventory"]["slot"][0] * i,
                    STARTING_POSITIONS["inventory"]["first_slot"][1]
                    + PIXEL_SIZES["inventory"]["slot"][1] * j,
                )
            )

            currency_location = locate_currency_in_currency_tab(
                currency_name=currency_name, by_image=True, by_text=None
            )
            if not currency_location:
                print(f"{currency_name} not found...")
                return

            pyautogui.moveTo(currency_location["position"])
            pyautogui.sleep(0.05)
            pyautogui.rightClick()
            pyautogui.sleep(0.05)

            middle_slot_x, middle_slot_y = STARTING_POSITIONS["stash"]["tabs"]["currency"][
                "middle_slot"
            ]
            position_offset = 30
            pyautogui.moveTo(
                middle_slot_x + random.randint(-position_offset, position_offset),
                middle_slot_y + random.randint(-position_offset, position_offset),
            )

            highlight_items(f'"{highlight_text}"')
            print("searching for", highlight_text)

            pyautogui.sleep(0.05)
            pyautogui.keyDown("shift")
            pyautogui.sleep(0.2)

            if currency_name == "chaos orb":
                random_pause_limit = int(random.uniform(90, 100))
                random_pause_delay = random.uniform(1.35, 2.15)
                craft_click_delay = random.uniform(0.2, 0.24)
                currency_quanitity_used_checkpoint = 1

            while True:

                craft_result = None

                if currency_quanitity_used % currency_quanitity_used_checkpoint == 0:
                    craft_result = get_craft_result()

                if craft_result:
                    pyautogui.sleep(0.1)
                    pyautogui.keyUp("shift")
                    move_item(position=pyautogui.position())

                    items_crafted += 1
                    break

                pyautogui.click()
                pyautogui.sleep(craft_click_delay)

                currency_quanitity_used += 1
                if currency_quanitity_used >= crafting_currency_available_quantity:
                    print("chaos orb limit reached....")
                    return True

                if currency_quanitity_used % random_pause_limit == 0:
                    pyautogui.sleep(0.05)
                    pyautogui.rightClick()
                    pyautogui.sleep(0.05)
                    currency_location = locate_currency_in_currency_tab(
                        currency_name=currency_name, by_image=True, by_text=None
                    )

                    is_middle_slot_empty = check_middle_slot()
                    if is_middle_slot_empty:
                        print("middle slot is empty...")
                        continue

                    if not currency_location:
                        print("chaos orb not found...")
                        return

                    pyautogui.moveTo(currency_location["position"])
                    pyautogui.sleep(0.05)
                    pyautogui.rightClick()
                    pyautogui.sleep(0.05)

                    middle_slot_x, middle_slot_y = STARTING_POSITIONS["stash"]["tabs"]["currency"][
                        "middle_slot"
                    ]
                    position_offset = 30
                    pyautogui.moveTo(
                        middle_slot_x + random.randint(-position_offset, position_offset),
                        middle_slot_y + random.randint(-position_offset, position_offset),
                        0.1,
                    )

                    pyautogui.sleep(random_pause_delay)


def currency_slam(
    craft_targets,
):
    focus_game()

    for craft_target in craft_targets:
        craft_items(craft_target)

    return True


item_to_craft_width = 1
item_to_craft_height = 1
crafting_currency_available_quantity = 16444
max_items_to_craft = 20
currency_name = "chaos orb"
# currency_name =
# highlight_text = "(4[7-9]|50).*spirit"
highlight_text = "(4[7-9]|50).*spirit|3 to level.*ell skills"
# highlight_text = "3 to level of all (proj.*|melee.*)lls"
# highlight_text = "4.*spell skills|4.*melee skills"
# highlight_text = "3 to level of all spell skills"
# highlight_text = "(4[7-9]|50).*rit|3.*melee.*lls|3.*proj.*lls"
# highlight_text = "(4[7-9]|50).*rit|4.*melee.*lls|3.*proj.*lls|3[5-9].*inc.*crit.*nus"
# highlight_text = "3[1-8].*spirit"
# highlight_text = "4.*minion skills"
# highlight_text = "3[5-9].*inc.*crit|6[1-5].*spirit|3[5-8].*spirit"
# highlight_text = "18([0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit|3.*spell skills"
# highlight_text = "1(6[5-9]|[7-8][0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit|3.*spell skills"
# highlight_text_minion = "3.*spell skills|3.*minion skills"
# highlight_text_minion = "1(6[5-9]|[7-8][0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit|3.*spell skills|3.*minion skills"

craft_targets = [
    {
        "currency_name": currency_name,
        "highlight_text": highlight_text,
        "crafting_currency_available_quantity": crafting_currency_available_quantity,
        "max_items_to_craft": max_items_to_craft,
        "item_to_craft_width": item_to_craft_width,
        "item_to_craft_height": item_to_craft_height,
    }
]

# craft_targets = [
#     {
#         "currency_name": "reaver catalyst",
#         "highlight_text": "quality.*40%",
#         "crafting_currency_available_quantity": crafting_currency_available_quantity,
#         "max_items_to_craft": max_items_to_craft,
#         "item_to_craft_width": item_to_craft_width,
#         "item_to_craft_height": item_to_craft_height,
#     },
#     {
#         "currency_name": "vaal catalysing infuser",
#         "highlight_text": "quality.*50%|corrupted",
#         "crafting_currency_available_quantity": crafting_currency_available_quantity,
#         "max_items_to_craft": max_items_to_craft,
#         "item_to_craft_width": item_to_craft_width,
#         "item_to_craft_height": item_to_craft_height,
#     },
# ]
currency_slam(craft_targets=craft_targets)
