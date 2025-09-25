import pyautogui
import time

pyautogui.PAUSE = 0.03

STARTING_COORDINATES = {
    "stash": {
        "location": {"x": 900, "y": 330},
        "slot": {"x": 31, "y": 131},
        "page": {"x": 780, "y": 150},
    },
    "npc": {"doryani": {"x": 700, "y": 450}},
    "inventory": {"slot": {"x": 1300, "y": 615}},
}

PIXEL_SIZES = {"inventory": {"slot": 52}, "stash": {"slot": 26, "page": 24}}
INVENTORY = {"rows": 31, "columns": 5}


def find_npc(npc_name):
    pyautogui.keyUp("ctrl")
    pyautogui.keyDown("alt")
    pyautogui.moveTo(
        STARTING_COORDINATES["npc"][npc_name]["x"],
        STARTING_COORDINATES["npc"][npc_name]["y"],
    )
    pyautogui.click()
    pyautogui.keyUp("alt")
    pyautogui.countdown(1)


def find_stash():
    pyautogui.moveTo(
        STARTING_COORDINATES["stash"]["location"]["x"],
        STARTING_COORDINATES["stash"]["location"]["y"],
    )
    pyautogui.click()


def from_inventory():
    pyautogui.keyDown("ctrl")
    for i in range(12):
        for j in range(5):
            pyautogui.moveTo(
                STARTING_COORDINATES["inventory"]["slot"]["x"]
                + PIXEL_SIZES["inventory"]["slot"] * i,
                STARTING_COORDINATES["inventory"]["slot"]["y"]
                + PIXEL_SIZES["inventory"]["slot"] * j,
            )
            pyautogui.click()

    pyautogui.keyUp("ctrl")


def from_stash(x, y):

    pyautogui.keyUp("ctrl")
    pyautogui.moveTo(
        STARTING_COORDINATES["stash"]["page"]["x"],
        STARTING_COORDINATES["stash"]["page"]["y"],
    )
    pyautogui.click()
    pyautogui.keyDown("ctrl")

    inventory_space, items_moved = 60, 0

    while x < 24:
        while y < 24:
            pyautogui.moveTo(
                STARTING_COORDINATES["stash"]["slot"]["x"]
                + PIXEL_SIZES["stash"]["slot"] * x,
                STARTING_COORDINATES["stash"]["slot"]["y"]
                + PIXEL_SIZES["stash"]["slot"] * y,
            )
            pyautogui.click()
            items_moved += 1
            if items_moved == inventory_space:
                pyautogui.keyUp("ctrl")
                return x, y

            y += 1
        x += 1
        y = 0


def sell_maps():

    item_count = input("How many items to sell: ")

    # focus the game
    pyautogui.click(1800, 1000)
    time.sleep(1)

    items_sold, x, y = 0, 0, 0

    while items_sold < int(item_count):
        find_stash()
        time.sleep(0.5)
        x, y = from_stash(x, y)
        print(x, y)
        pyautogui.press("esc")
        time.sleep(0.5)
        find_npc("doryani")
        from_inventory()
        pyautogui.press("esc")
        time.sleep(0.5)
        items_sold += 60


sell_maps()
