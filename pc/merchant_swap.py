from utility.config import (
    REGIONS,
    FOLDER_PATHS,
    IMAGE_NAMES,
    STARTING_POSITIONS,
    PIXEL_SIZES,
)
from utility.locate_image import locate_image
from utility.focus_game import focus_game
import pyautogui

pyautogui.PAUSE = 0


def move_items_from_inventory():
    # pyautogui.keyDown("ctrl")
    # pyautogui.sleep(0.005)
    # for i in range(0, 12, 2):
    #     for j in range(1, 5, 3):
    for i in range(0, 5, 2):
        for j in range(0, 1, 1):
            pyautogui.moveTo(
                STARTING_POSITIONS["inventory"]["first_slot"][0]
                + PIXEL_SIZES["inventory"]["slot"][0] * i,
                STARTING_POSITIONS["inventory"]["first_slot"][1]
                + PIXEL_SIZES["inventory"]["slot"][1] * j,
            )
            pyautogui.sleep(0.005)
            pyautogui.rightClick()
            pyautogui.sleep(0.005)


def move_items_from_merchant_tab():
    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.05)
    for i in range(3, 0, -2):
        for j in range(12, 0, -1):
            pyautogui.moveTo(
                STARTING_POSITIONS["npcs"]["ange"]["merchant"]["first_slot_selling"][0]
                + PIXEL_SIZES["inventory"]["slot"][0] * i,
                STARTING_POSITIONS["npcs"]["ange"]["merchant"]["first_slot_selling"][1]
                + PIXEL_SIZES["inventory"]["slot"][1] * j,
            )
            pyautogui.sleep(0.005)
            pyautogui.click()
            pyautogui.sleep(0.01)

    pyautogui.sleep(0.005)
    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.01)


def merchant_swap(option):
    # look for empty slot

    slot_size = PIXEL_SIZES["inventory"]["slot"][1]

    second_row_second_col = (
        REGIONS["npcs"]["ange"]["merchant"]["first_slot_selling"][0] + slot_size,
        REGIONS["npcs"]["ange"]["merchant"]["first_slot_selling"][1] + slot_size,
        REGIONS["npcs"]["ange"]["merchant"]["first_slot_selling"][2],
        REGIONS["npcs"]["ange"]["merchant"]["first_slot_selling"][3],
    )
    print(second_row_second_col)
    focus_game()
    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.05)
    while True:

        if option == "spam":
            while True:
                move_items_from_inventory()

        res = locate_image(
            region=second_row_second_col,
            image_name=IMAGE_NAMES["npcs"]["ange"]["merchant"]["empty_slot_selling"],
            folder_path=FOLDER_PATHS["assets"]["images"]["npcs"]["ange"]["merchant"],
            confidence=0.75,
            constant_focus=False,
        )

        if res["is_found"]:

            while True:
                move_items_from_inventory()
                pyautogui.keyUp("ctrl")
                pyautogui.sleep(0.05)
                pyautogui.sleep(1.5)
                move_items_from_merchant_tab()
                exit()

            # when empty, insert new item


merchant_swap(option="spam")
