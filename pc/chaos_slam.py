import pyautogui
from utility.config import REGIONS, FOLDER_PATHS, IMAGE_NAMES, STARTING_POSITIONS
from utility.inventory_management import select_currency_in_inventory
from utility.locate_image import locate_image
from utility.stash_management import highlight_items

pyautogui.PAUSE = 0.005


def get_craft_result():
    image_res = locate_image(
        region=REGIONS["stash"]["tabs"]["currency"]["middle_extra_slot_area"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["tabs"]["currency"],
        image_name=IMAGE_NAMES["stash"]["tabs"]["currency"]["highlight"],
        constant_focus=False,
    )

    print(image_res["is_found"])

    if image_res["is_found"]:
        return image_res


def select_chaos_orb():
    image_res = select_currency_in_inventory("chaos_orb")

    return image_res["is_found"]


def chaos_slam(highlight_text):
    chaos_orb_selected = select_chaos_orb()
    print(chaos_orb_selected)
    if not chaos_orb_selected:
        print("chaos not found...")
        return
    # highlight_items('"3 to level of all spell skills"')
    highlight_items(f'"{highlight_text}"')
    pyautogui.keyDown("shift")
    pyautogui.sleep(0.05)
    pyautogui.moveTo(
        STARTING_POSITIONS["stash"]["tabs"]["currency"]["extra_middle_slot"]
    )
    pyautogui.sleep(0.05)

    while True:

        pyautogui.click()
        pyautogui.sleep(0.2)

        craft_result = get_craft_result()

        if craft_result:
            pyautogui.keyUp("shift")
            pyautogui.sleep(0.05)
            break


chaos_slam(highlight_text="(4[7-9]|50) to spirit|3 to level of all spell skills")
