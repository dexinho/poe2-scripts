import pyautogui
pyautogui.PAUSE = 0.014

STARTING_COORDINATES = {
    "stash": {
        "location": {"x": 900, "y": 330},
        "item": {"x": 43, "y": 140},
        "page": {"x": 790, "y": 150},
    },
    "npc": {"x": 700, "y": 450},
    "inventory": {"item": {"x": 1300, "y": 615}},
}

PIXEL_SIZES = {"inventory": {"slot": 53}, "stash": {"page": 24}}
INVENTORY = {"rows": 12, "columns": 5}

def fromInv(inventory):
    itemsMoved = 0
    pyautogui.keyDown("ctrl")
    for i in range(inventory["rows"]):
        for j in range(inventory["columns"]):
            pyautogui.moveTo(
                STARTING_COORDINATES["inventory"]["item"]["x"]
                + PIXEL_SIZES["inventory"]["slot"] * i,
                STARTING_COORDINATES["inventory"]["item"]["y"]
                + PIXEL_SIZES["inventory"]["slot"] * j,
            )
            pyautogui.click()
            itemsMoved += 1

            if itemsMoved == inventory["number_of_items"]:
                pyautogui.keyUp("ctrl")
                return None

    pyautogui.keyUp("ctrl")
    
fromInv(
    {
        "rows": 12,
        "columns": 5,
        "number_of_items": 60,
    }
)
