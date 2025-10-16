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
            "main": BASE_PATH / "assets" / "images" / "main",
            "inventory": {
                "currencies": BASE_PATH
                / "assets"
                / "images"
                / "inventory"
                / "currencies"
            },
            "craft": BASE_PATH / "assets" / "images" / "craft",
            "items": BASE_PATH / "assets" / "images" / "items",
            "loading": BASE_PATH / "assets" / "images" / "loading",
            "stash": {
                "main": BASE_PATH / "assets" / "images" / "stash" / "main",
                "tabs": {
                    "currency": BASE_PATH
                    / "assets"
                    / "images"
                    / "stash"
                    / "tabs"
                    / "currency"
                },
            },
            "npcs": {
                "doryani": {
                    "buy_or_sell_items": BASE_PATH
                    / "assets"
                    / "images"
                    / "npcs"
                    / "doryani"
                },
                "gwennen": {
                    "deal": BASE_PATH
                    / "assets"
                    / "images"
                    / "npcs"
                    / "gwennen"
                    / "deal"
                },
                "ange": {
                    "currency_exchange": BASE_PATH
                    / "assets"
                    / "images"
                    / "npcs"
                    / "ange"
                    / "currency_exchange"
                },
            },
        }
    }
}


IMAGE_NAMES = {
    "main": {
        "icon": "icon.png",
        "character_active": "character_active.png",
        "login_button": "login_button.png",
        "play_button": "play_button.png",
    },
    "npcs": {
        "doryani": {"buy_or_sell_items": {"logo": "logo.png"}},
        "gwennen": {
            "deal": {
                "exit_button": "exit_button.png",
                "item_craft_window": "item_craft_window.png",
                "item_highlight": "item_highlight.png",
                "logo": "logo.png",
            }
        },
        "ange": {
            "currency_exchange": {
                "order_completed": "order_completed.png",
                "logo": "logo.png",
            }
        },
    },
    "inventory": {
        "currencies": {
            "exalted_orb": "exalted_orb.png",
            "orb_of_annulment": "orb_of_annulment.png",
            "orb_of_alchemy": "orb_of_alchemy.png",
            "orb_of_chance": "orb_of_chance.png",
            "divine_orb": "divine_orb.png",
            "chaos_orb": "chaos_orb.png",
        },
    },
    "items": {
        "item_highlight": "item_highlight.png",
        "item_highlight_2": "item_highlight_2.png",
        "item_highlight_3": "item_highlight_3.png",
        "item_highlight_4": "item_highlight_4.png",
    },
    "merchant": {
        "logo": "merchant_logo.png",
        "item_highlight": "item_highlight.png",
    },
    "loading": {"loading_screen": "loading_screen.png"},
    "craft": {"item_highlight": "item_highlight.png"},
    "stash": {
        "main": {"logo": "logo.png"},
        "tabs": {"currency": {"highlight": "highlight.png"}},
    },
}

STARTING_POSITIONS = {
    "stash": {
        "position": (1111, 377),
        "tabs": {
            "first_slot": (750, 100),
            "currency": {"extra_middle_slot": (330, 440)},
        },
    },
    "npcs": {
        "gwennen": {
            "position": (785, 333),
            "buy_button": (625, 755),
            "take_item_button": (450, 750),
            "refresh_shop_button": (950, 880),
        },
        "doryani": {
            "position": (975, 280),
            "buy_button": (625, 755),
            "take_item_button": (450, 750),
        },
        "ange": {
            "position": (1200, 470),
        },
    },
    "inventory": {
        "first_slot": (1300, 615),
    },
}

REGIONS = {
    "main": {
        "login_button": (920, 890, 100, 100),
        "play_button": (710, 950, 100, 100),
        "character_active": (10, 990, 100, 100),
    },
    "npcs": {
        "doryani": {"buy_or_sell": (930, 180, 50, 50)},
        "gwennen": {
            "deal": {
                "exit_button": (930, 180, 50, 50),
                "item_craft_window": (590, 360, 50, 50),
                "area": (300, 270, 640, 640),
                "logo": (620, 180, 20, 20),
            }
        },
        "ange": {
            "currency_exchange": {
                "orders": (260, 370, 1030, 560),
                "logo": (555, 165, 400, 20),
            },
        },
    },
    "stash": {
        "tabs": {
            "currency": {
                "area": (15, 120, 650, 630),
                "middle_extra_slot_area": (285, 360, 100, 170),
                "bottom_extra_slots_area": (120, 620, 340, 130),
            }
        },
        "main": {"logo": (325, 5, 20, 20)},
    },
    "inventory": {"area": (1270, 590, 640, 260)},
    "merchant": {"area": (305, 220, 640, 640), "logo": (622, 130, 8, 8)},
    "loading": {"loading_screen": (1250, 850, 300, 300)},
}

PIXEL_SIZES = {
    "inventory": {"slot": (53, 53)},
    "stash": {"tab": (130, 25)},
    "currency_exchange": {"slot": (53, 53), "order": (330, 100)},
}

HIDEOUT_OWNERS = {
    "djumbircic": "shoreline hideout",
    "muldrotha_gravetide": "limestone hideout",
    "telroy": "shrine hideout",
    "followwitch": "plateau of the gods hideout",
    "": "canal hideout",
}

total_items_bought = 0
item_purchase_quantity = 7
refresh_shop_trehshold = item_purchase_quantity * 2
hideout_refresh_treshold = refresh_shop_trehshold * 150

GENERATE_GOLD_DATA = {
    "is_characater_active": False,
    "is_search_active": False,
    "is_hideout_changed": False,
    "is_game_focused": False,
    "total_items_bought": total_items_bought,
    "refresh_shop_trehshold": refresh_shop_trehshold,
    "item_purchase_quantity": item_purchase_quantity,
    "hideout_refresh_treshold": hideout_refresh_treshold,
    "hideout_owner_name": "djumbircic",
    "hideout_owner_name_backup": "telroy",
    "gold_tab_slot_position": 1,
}
