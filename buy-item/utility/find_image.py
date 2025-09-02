import pyautogui
import os


def find_image(region, folder, image_name):
    image_path = os.path.join(folder, image_name)
    
    try:
        location = pyautogui.locateOnScreen(image=image_path, region=region, confidence=0.99)
        center = pyautogui.center(location)
        return {"is_found": True, "position": {"x": center.x, "y": center.y}}

    except pyautogui.ImageNotFoundException:
        return {"is_found": False, "position": None}
