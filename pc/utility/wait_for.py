import pyautogui
from utility.errors import PoeCharacterNotActive, PoeCharacterBugged


def wait_for(callback, *args, wait_attempt_threshold=10, delay=1):
    from utility.poe2_main import character_active
    for wait_attempt in range(wait_attempt_threshold):
        if wait_attempt > 0:
            print(f"Waiting attempt: {wait_attempt}")
        if callback(*args):
            return True
        pyautogui.sleep(delay)

    if character_active():
        raise PoeCharacterBugged(
            f"Timeout waiting for {callback.__name__}. Character bugged."
        )

    raise PoeCharacterNotActive(
        f"Timeout waiting for {callback.__name__}. Character not active."
    )
