import pyautogui
from utility.errors import PoeCharacterNotActive, PoeCharacterBugged


def wait_for(callback, *args, wait_attempt_threshold=10, delay=1):
    from utility.main import character_active

    for wait_attempt in range(wait_attempt_threshold):
        if wait_attempt > 0:
            print(f"Waiting attempt: {wait_attempt}")
        callback_res = callback(*args)
        if callback_res:
            return callback_res
        pyautogui.sleep(delay)

    if character_active():
        raise PoeCharacterBugged(
            f"Timeout waiting for {callback.__name__}. Character bugged."
        )

    raise PoeCharacterNotActive(
        f"Timeout waiting for {callback.__name__}. Character not active."
    )
