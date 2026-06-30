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

pyautogui.PAUSE = 0.005


def get_craft_result():
    image_res = locate_image(
        region=REGIONS["stash"]["tabs"]["currency"]["middle_slot_area"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["currency"],
        image_name=IMAGE_NAMES["stash"]["tabs"]["currency"]["middle_slot_highlight"],
        constant_focus=False,
    )

    return image_res


def select_chaos_orb():
    image_res = select_currency_in_inventory("chaos_orb")

    return image_res


def chaos_slam(
    highlight_text,
    tab,
    max_items_to_craft,
    chaos_orbs_available,
    item_to_craft_width=1,
    item_to_craft_height=1,
):
    focus_game()
    chaos_orb_name = "chaos orb"
    chaos_orb_used = 0
    items_crafted = 0

    # chaos_orb_selected = select_chaos_orb()
    # if not chaos_orb_selected:
    #     print("chaos not found...")
    #     return

    for i in range(0, 12, item_to_craft_width):
        for j in range(0, 5, item_to_craft_height):
            if items_crafted >= max_items_to_craft:
                print("item craft limit reached...")
                return True

            pyautogui.moveTo(
                STARTING_POSITIONS["inventory"]["first_slot"][0]
                + PIXEL_SIZES["inventory"]["slot"][0] * i,
                STARTING_POSITIONS["inventory"]["first_slot"][1]
                + PIXEL_SIZES["inventory"]["slot"][1] * j,
            )
            pyautogui.keyDown("ctrl")
            pyautogui.sleep(0.1)
            pyautogui.click()
            pyautogui.sleep(0.1)
            pyautogui.keyUp("ctrl")
            pyautogui.sleep(0.1)

            chaos_orb_location = locate_currency_in_currency_tab(
                currency_name=chaos_orb_name, by_image=True, by_text=None
            )
            if not chaos_orb_location:
                print("chaos orb not found...")
                return

            pyautogui.moveTo(chaos_orb_location["position"])
            pyautogui.sleep(0.1)
            pyautogui.rightClick()
            pyautogui.sleep(0.1)

            if tab == "currency":
                base_x, base_y = STARTING_POSITIONS["stash"]["tabs"]["currency"][
                    "middle_slot"
                ]
                position_offset = 30
                pyautogui.moveTo(
                    base_x + random.randint(-position_offset, position_offset),
                    base_y + random.randint(-position_offset, position_offset),
                )

            highlight_items(f'"{highlight_text}"')
            print("searching for", highlight_text)

            pyautogui.sleep(0.1)
            pyautogui.keyDown("shift")
            pyautogui.sleep(0.1)

            random_pause_limit = int(random.uniform(90, 100))

            while True:

                craft_result = get_craft_result()

                if craft_result:
                    pyautogui.sleep(0.1)
                    pyautogui.keyUp("shift")
                    pyautogui.sleep(0.1)
                    pyautogui.keyDown("ctrl")
                    pyautogui.sleep(0.1)
                    pyautogui.click()
                    pyautogui.sleep(0.1)
                    pyautogui.keyUp("ctrl")
                    pyautogui.sleep(0.1)

                    items_crafted += 1
                    break

                pyautogui.click()
                pyautogui.sleep(random.uniform(0.2, 0.24))

                chaos_orb_used += 1
                if chaos_orb_used >= chaos_orbs_available:
                    print("chaos orb limit reached....")
                    return True

                if chaos_orb_used % random_pause_limit == 0:
                    pyautogui.rightClick()
                    pyautogui.sleep(0.1)
                    chaos_orb_location = locate_currency_in_currency_tab(
                        currency_name=chaos_orb_name, by_image=True, by_text=None
                    )

                    if not chaos_orb_location:
                        print("chaos orb not found...")
                        return

                    pyautogui.moveTo(chaos_orb_location["position"])
                    pyautogui.sleep(0.1)
                    pyautogui.rightClick()
                    pyautogui.sleep(0.1)

                    if tab == "currency":
                        base_x, base_y = STARTING_POSITIONS["stash"]["tabs"][
                            "currency"
                        ]["middle_slot"]
                        position_offset = 30
                        pyautogui.moveTo(
                            base_x + random.randint(-position_offset, position_offset),
                            base_y + random.randint(-position_offset, position_offset),
                            0.02,
                        )

                    pyautogui.sleep(random.uniform(1.4, 2.2))

    return True


highlight_text = "4 to level of all spell skills"
# highlight_text = "(4[7-9]|50).*spirit|4 to level of all spell skills"
# highlight_text = "18([0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit|3.*spell skills"
# highlight_text = "1(6[5-9]|[7-8][0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit|3.*spell skills"
# highlight_text_minion = "3.*spell skills|3.*minion skills"
# highlight_text_minion = "1(6[5-9]|[7-8][0-9]).*max.*mana|[7-8]%.*max.*mana|(4[7-9]|50).*spirit|3.*spell skills|3.*minion skills"
chaos_slam(
    highlight_text=highlight_text,
    tab="currency",
    max_items_to_craft=5,
    chaos_orbs_available=12000,
)

# 29 OOL 29 WIT 30d
