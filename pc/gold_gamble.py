import pyautogui
from utility.text_from_image import read_text_from_image
from utility.locate_image import locate_image
from utility.focus_game import focus_game
from utility.config import (
    REGIONS,
    FOLDER_PATHS,
    IMAGE_NAMES,
    STARTING_POSITIONS,
    PIXEL_SIZES,
)


def gold_gamble():
    count = 0
    focus_game()
    while True:

        mouse_position = pyautogui.position()
        x_offset = -5
        y_offset = -65
        width = 60
        height = 25
        region = (
            mouse_position[0] + x_offset,
            mouse_position[1] + y_offset,
            width,
            height,
        )
        count += 1
        text = read_text_from_image(region=region)
        print("text:", text)
        print(count, region)
        pyautogui.sleep(0.2)


gold_gamble()
