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
            "currency": BASE_PATH / "assets" / "images" / "currency",
            "craft": BASE_PATH / "assets" / "images" / "craft",
            "items": BASE_PATH / "assets" / "images" / "items",
            "merchant": BASE_PATH / "assets" / "images" / "merchant",
            "loading": BASE_PATH / "assets" / "images" / "loading",
        }
    }
}

REGIONS = {
    "stash": {"area": (15, 120, 650, 630)},
    "inventory": {"area": (1270, 590, 640, 260)},
    "merchant": {"area": (305, 220, 640, 640), "logo": (622, 130, 8, 8)},
    "loading": {"loading_screen": (1250, 850, 300, 300)},
}

FILE_NAMES = {
    "assets": {
        "images": {
            "currency": {"chaos_orb": "chaos_orb.png"},
            "items": {
                "item_highlight": "item_highlight.png",
                "item_highlight_2": "item_highlight_2.png",
                "item_highlight_3": "item_highlight_3.png",
                "item_highlight_4": "item_highlight_4.png",
            },
            "merchant": {"logo": "merchant_logo.png"},
            "loading": {"loading_screen": "loading_screen.png"},
            "craft": {"item_highlight": "item_highlight.png"},
        }
    }
}

HIDEOUT_OWNERS = {
    "djumbircic": "felled hideout",
    "tokks": "shoreline hideout",
    "muldrotha_gravetide": "limestone hideout",
    "telroy": "shrine hideout",
    "": "canal hideout",
}

PIXEL_SIZES = {"inventory": {"slot": 53}}
