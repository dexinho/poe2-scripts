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
            "crafts": {
                "desecrate": BASE_PATH / "assets" / "images" / "crafts" / "desecrate",
            },
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
                    / "currency",
                    "quad": BASE_PATH / "assets" / "images" / "stash" / "tabs" / "quad",
                    "basic": BASE_PATH
                    / "assets"
                    / "images"
                    / "stash"
                    / "tabs"
                    / "basic",
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
                    / "currency_exchange",
                    "merchant": BASE_PATH
                    / "assets"
                    / "images"
                    / "npcs"
                    / "ange"
                    / "merchant",
                    "buy_or_sell_items": BASE_PATH
                    / "assets"
                    / "images"
                    / "npcs"
                    / "ange"
                    / "buy_or_sell_items",
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
                "refresh_shop_button": "refresh_shop_button.png",
                "purchase_window": "purchase_window.png",
                "deal_window": "deal_window.png",
            }
        },
        "ange": {
            "currency_exchange": {
                "order_completed": "order_completed.png",
                "logo": "logo.png",
            },
            "merchant": {
                "logo_buying": "logo_buying.png",
                "item_sold_notification_x_button": "item_sold_notification_x_button.png",
                "empty_slot_selling": "empty_slot_selling.png",
                "item_highlight_1": "item_highlight_1.png",
                "item_highlight_2": "item_highlight_2.png",
                "item_highlight_3": "item_highlight_3.png",
                "item_highlight_4": "item_highlight_4.png",
            },
            "buy_or_sell_items": {
                "logo": "logo.png",
                "gold_symbol_1": "gold_symbol_1.png",
                "gold_symbol_2": "gold_symbol_2.png",
            },
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
            "omen_of_bartering": "omen_of_bartering.png",
            "perfect_essence_of_the_infinite": "perfect_essence_of_the_infinite.png",
            "preserved_collarbone": "preserved_collarbone.png",
            "ancient_collarbone": "ancient_collarbone.png",
            "runic_alloy": "runic_alloy.png",
            "perfect_essence_of_enhancment": "perfect_essence_of_enhancment.png",
        },
    },
    "loading": {"loading_screen": "loading_screen.png"},
    "crafts": {
        "item_highlight": "item_highlight.png",
        "desecrate": {
            "desecrated_modifiers_tooltip_popup": "desecrated_modifiers_tooltip_popup.png",
            "third_choice_bottom_right_corner": "third_choice_bottom_right_corner.png",
        },
    },
    "stash": {
        "main": {"logo": "logo.png"},
        "tabs": {
            "currency": {
                "highlight": "highlight.png",
                "middle_slot_highlight": "middle_slot_highlight.png",
                "middle_slot_empty": "middle_slot_empty.png",
                "chaos_orb": "chaos_orb.png",
                "vaal_catalysing_infuser": "vaal_catalysing_infuser.png",
                "sibilant_catalyst": "sibilant_catalyst.png",
                "reaver_catalyst": "reaver_catalyst.png",
            },
            "quad": {"highlight": "highlight.png", "empty_slot": "empty_slot.png"},
            "basic": {"highlight": "highlight.png"},
        },
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
                "refresh_shop_button": (920, 855, 50, 50),
                "item_craft_window": (590, 360, 50, 50),
                "area": (300, 270, 640, 640),
                "logo": (620, 180, 20, 20),
                "deal_window": (618, 318, 20, 20),
                "purchase_window": (618, 318, 20, 20),
            }
        },
        "ange": {
            "currency_exchange": {
                "orders": (260, 370, 1030, 560),
                "logo": (555, 165, 400, 20),
                "market_ratio": (920, 230, 80, 18),
                "i_want": (640, 220, 175, 40),
                "i_have": (1140, 220, 175, 40),
                "popular": (735, 175, 665, 185),
                "tab_currency_text": (775, 180, 170, 35),
            },
            "merchant": {
                "area_buying": (305, 220, 640, 640),
                "first_slot_selling": (35, 183, 15, 15),
                "logo_buying": (622, 128, 10, 12),
                "item_sold_notification_x_button": (1125, 450, 200, 400),
            },
            "buy_or_sell_items": {
                "logo": (600, 180, 400, 20),
                "gold_symbol_1": (100, 250, 1100, 100),
                "gold_symbol_2": (100, 400, 1100, 100),
            },
        },
    },
    "stash": {
        "tabs": {
            "currency": {
                "area": (15, 120, 650, 630),
                "middle_slot_area": (290, 365, 80, 160),
                "middle_slot_top_left_area": (290, 365, 20, 20),
                "bottom_extra_slots_area": (120, 620, 340, 130),
            },
            "quad": {"area": (15, 120, 635, 640)},
            "basic": {"area": (12, 122, 645, 650)},
        },
        "main": {"logo": (325, 5, 20, 20)},
    },
    "inventory": {"area": (1270, 590, 640, 260)},
    "loading": {"loading_screen": (1250, 850, 300, 300)},
    "crafts": {
        "desecrate": {
            "options_area": (400, 610, 250, 200),
            "desecrated_modifiers_tooltip_popup": (340, 250, 500, 500),
            "third_choice_bottom_right_corner": (830, 780, 77, 66),
        },
    },
}

STARTING_POSITIONS = {
    "stash": {
        "position": (1110, 375),
        "tabs": {
            "first_slot": (750, 100),
            "currency": {"middle_slot": (330, 440)},
            "quad": {"first_slot": (14, 125)},
        },
    },
    "npcs": {
        "gwennen": {
            "position": (785, 333),
            "buy_button": (625, 755),
            "take_item_button": (450, 750),
            "refresh_shop_button": (950, 880),
            "area": {
                "first_slot": (333, 300),
            },
        },
        "doryani": {
            "position": (975, 280),
            "buy_button": (625, 755),
            "take_item_button": (450, 750),
        },
        "ange": {
            "position": (1200, 470),
            "merchant": {"first_slot_selling": (40, 185)},
            "buy_and_sell_items": {"area": (980, 560)},
            "currency_exchange": {
                "i_want": (710, 240),
                "i_have": (1200, 240),
                "found_currency": (820, 195),
                "tabs": {"popular": (600, 205)},
                "search_x_button": (1395, 112),
            },
        },
    },
    "inventory": {
        "first_slot": (1300, 615),
    },
    "crafts": {
        "desecrate": {
            "reveal_button": (625, 855),
            "confirm_button": (625, 855),
            "reroll_button": (870, 855),
            "item_slot": (630, 460),
        },
    },
}

PIXEL_SIZES = {
    "inventory": {"slot": (53, 53)},
    "stash": {"tab": (130, 24), "tabs": {"quad": {"slot": (26.25, 26.25)}}},
    "currency_exchange": {"slot": (53, 53), "order": (330, 100)},
}

HIDEOUT_OWNERS = {
    "korozijaroa": "shoreline hideout",
    "": "canal hideout",
}

total_items_bought = 0
item_purchase_quantity = 13
refresh_shop_trehshold = item_purchase_quantity * 2
hideout_refresh_treshold = refresh_shop_trehshold * 100

GENERATE_GOLD_DATA = {
    "action_delay": 0.0102,
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
    "gold_tab_slot_position": 0,
}
