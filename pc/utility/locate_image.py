import pyautogui
import os

from utility.config import DISPLAY_SETTINGS


def locate_image(
    folder_path,
    image_name,
    confidence=0.99,
    region=(
        0,
        0,
        DISPLAY_SETTINGS["reference_width"],
        DISPLAY_SETTINGS["reference_height"],
    ),
):
    pyautogui.moveTo(3, 3)
    pyautogui.sleep(0.01)

    image_path = os.path.join(folder_path, image_name)

    try:
        location = pyautogui.locateOnScreen(
            image=image_path, region=region, confidence=confidence
        )
        center = pyautogui.center(location)
        return {"is_found": True, "position": (center.x, center.y)}

    except pyautogui.ImageNotFoundException:
        return {"is_found": False, "position": None}
