import pyautogui
import keyboard
from utility.config import IMAGE_NAMES, FOLDER_PATHS, REGIONS
from utility.locate_image import locate_image
from utility.wait_for import wait_for


def click_icon():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["icon"],
        confidence=0.9
    )
    
    if image_res:
        pyautogui.moveTo(1, 1)
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(0.1)
        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.5)
        pyautogui.click()
        pyautogui.sleep(0.5)
        pyautogui.press("enter")
        pyautogui.sleep(10)
        return image_res

    return None


def click_login():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["login_button"],
        region=REGIONS["main"]["login_button"],
        confidence=0.9,
    )

    if image_res:
        # if disconnected/failed to connect to instance pops up
        pyautogui.moveTo(960, 565)
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(1)

        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(2)
        return image_res

    return None


def click_play():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["play_button"],
        region=REGIONS["main"]["play_button"],
        confidence=0.9,
    )

    if image_res:
        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(5)
        return image_res

    return None


def character_active():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["character_active"],
        region=REGIONS["main"]["character_active"],
        confidence=0.9,
    )

    return image_res


def enter_game(max_retries=100, delay=0.1):
    for attempt in range(max_retries):
        print(f"Entering the game (attempt {attempt + 1}/{max_retries})")
        click_icon()
        click_login()
        if click_play():
            print("Entered game successfully.")
            return True

        pyautogui.sleep(delay)

        if attempt == max_retries - 1:
            print("Icon not found, switching desktop...")
            keyboard.press_and_release("windows+d")
            pyautogui.sleep(1)
            return None


def start_poe2(max_retries=10):
    for attempt in range(max_retries):
        try:
            print(f"Starting PoE2 (attempt {attempt + 1}/{max_retries})")

            wait_for(enter_game, wait_attempt_threshold=100)
            wait_for(character_active, wait_attempt_threshold=100)

            print("PoE2 started successfully.")
            return True

        except Exception as e:
            print(f"Error while starting PoE2: {e}")
            exit()

    print("Failed to start PoE2 after multiple attempts.")
    exit()
