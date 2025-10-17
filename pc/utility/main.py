import pyautogui
import keyboard
from utility.config import IMAGE_NAMES, FOLDER_PATHS, REGIONS
from utility.locate_image import locate_image
from utility.wait_for import wait_for


def click_login():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["login_button"],
        region=REGIONS["main"]["login_button"],
        confidence=0.9,
    )

    if image_res["is_found"]:
        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(0.1)
        return image_res

    return None


def click_play():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["play_button"],
        region=REGIONS["main"]["play_button"],
        confidence=0.9,
    )

    if image_res["is_found"]:
        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(0.1)
        return image_res

    return None


def character_active():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["character_active"],
        region=REGIONS["main"]["character_active"],
        confidence=0.9,
    )

    if image_res["is_found"]:
        return image_res

    return None


def click_icon():
    image_res = locate_image(
        folder_path=FOLDER_PATHS["assets"]["images"]["main"],
        image_name=IMAGE_NAMES["main"]["icon"],
    )

    if image_res["is_found"]:
        pyautogui.moveTo(1, 1)
        pyautogui.sleep(0.1)
        pyautogui.click()
        pyautogui.sleep(0.1)
        pyautogui.moveTo(image_res["position"])
        pyautogui.sleep(0.5)
        pyautogui.click()
        pyautogui.sleep(0.5)
        pyautogui.press("enter")
        pyautogui.sleep(0.5)
        return image_res

    return None


def start_poe2(max_retries=10):
    for attempt in range(max_retries):
        try:
            print(f"Starting PoE2 (attempt {attempt + 1}/{max_retries})")

            if not click_icon():
                print("Icon not found, switching desktop...")
                keyboard.press_and_release("windows+d")
                pyautogui.sleep(1)
                continue

            wait_for(click_login, wait_attempt_threshold=60)
            wait_for(click_play, wait_attempt_threshold=20)
            wait_for(character_active, wait_attempt_threshold=30)

            print("PoE2 started successfully.")
            return True

        except Exception as e:
            print(f"Error while starting PoE2: {e}")
            exit()

    print("Failed to start PoE2 after multiple attempts.")
    exit()
