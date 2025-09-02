import pyautogui
import os

from utility.config import REGIONS, FOLDER_PATHS, FILE_NAMES
# pyautogui.moveTo(312, 223, 0.5)
region = (417, 224, 1, 157)
path = FOLDER_PATHS['assets']['images']['items']
image_name = FILE_NAMES['assets']['images']['items']['item_highlight_3']
full_path = os.path.join(path, image_name)
screenshot = pyautogui.screenshot(region=region)
screenshot.save(full_path)