import pyautogui
from pathlib import Path

display_width, display_height = pyautogui.size()
DISPLAY_SETTINGS = {
    "reference_width": 1920,
    "reference_height": 1080,
    "display_width": display_width,
    "display_height": display_height,
}

BASE_PATH = Path(__file__).resolve().parent.parent
FOLDER_PATHS = {
    "assets": {
        "images": {
            "items": BASE_PATH / "assets" / "images" / "items",
            "merchant": BASE_PATH / "assets" / "images" / "merchant",
        }
    }
}

REGIONS = {"merchant": {"area": (305, 220, 640, 640), "logo": (610, 125, 30, 30)}}

FILE_NAMES = {
    "assets": {
        "images": {
            "items": {
                "item_highlight": "item_highlight.png",
                "item_highlight_2": "item_highlight_2.png",
                "item_highlight_3": "item_highlight_3.png",
                "item_highlight_4": "item_highlight_4.png",
            },
            "merchant": {"logo": "merchant_logo.png"},
        }
    }
}


PIXEL_SIZES = {"inventory": {"slot": 53}}
