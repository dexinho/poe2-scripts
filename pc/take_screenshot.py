import pyautogui
import os

from utility.config import REGIONS, FOLDER_PATHS, IMAGE_NAMES
# pyautogui.moveTo(312, 223, 0.5)
region = (417, 224, 1, 157)
path = FOLDER_PATHS['assets']['images']['items']
image_name = IMAGE_NAMES['items']['item_highlight_223']
full_path = os.path.join(path, image_name)
screenshot = pyautogui.screenshot(region=region)
screenshot.save(full_path)