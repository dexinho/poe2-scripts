import pyautogui
from utility.locate_image import locate_image
from utility.config import (
    IMAGE_NAMES,
    FOLDER_PATHS,
    REGIONS,
    STARTING_POSITIONS,
)


def open_stash():
    print(f"Opening stash...")
    pyautogui.moveTo(STARTING_POSITIONS["stash"]["position"])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)
    image_res = locate_image(
        region=REGIONS["stash"]["main"]["logo"],
        folder_path=FOLDER_PATHS["assets"]["images"]["stash"]["main"],
        image_name=IMAGE_NAMES["stash"]["main"]["logo"],
    )

    if image_res["is_found"]:
        return image_res

    return None


def open_npc_shop(npc):
    npc_name = npc["name"]
    npc_option = npc["option"]
    print(f"Opening {npc_name}'s {npc_option}...")
    pyautogui.keyDown("alt")
    pyautogui.sleep(0.02)
    pyautogui.moveTo(STARTING_POSITIONS["npcs"][npc_name]["position"])
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.keyUp("alt")
    pyautogui.sleep(0.15)

    npc_logo_res = locate_image(
        region=REGIONS["npcs"][npc_name][npc_option]["logo"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"][npc_name][npc_option],
        image_name=IMAGE_NAMES["npcs"][npc_name][npc_option]["logo"],
    )

    if npc_logo_res["is_found"]:
        return npc_logo_res

    # somepyautoguis it struggles to find logo, this is backup that fixes it
    if not npc_name == "gwennen":
        return None

    refresh_shop_res = locate_image(
        region=REGIONS["npcs"]["gwennen"]["deal"]["logo"],
        folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["gwennen"]["deal"],
        image_name=IMAGE_NAMES["npcs"]["gwennen"]["deal"]["refresh_shop_button"],
        confidence=0.85,
    )

    if refresh_shop_res["is_found"]:
        pyautogui.moveTo(refresh_shop_res)
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(0.5)
        print("Gwennen's shop bugged!")

        return refresh_shop_res
