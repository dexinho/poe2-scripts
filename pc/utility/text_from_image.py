import mss
import numpy as np
import cv2
import pytesseract
import re
from PIL import Image

from utility.config import DISPLAY_SETTINGS

sct = mss.mss()


def read_text_from_image(region):
    with mss.MSS() as sct:
        screenshot = sct.grab(region)

        img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")

        text = pytesseract.image_to_string(img)
        return text


def currency_exchange_text_from_image(
    region=(
        0,
        0,
        DISPLAY_SETTINGS["reference_width"],
        DISPLAY_SETTINGS["reference_height"],
    ),
    whitelist=None,
    psm=1,
    fx=2,
    fy=2,
):
    x, y, w, h = region

    screenshot = sct.grab(
        {
            "left": x,
            "top": y,
            "width": w,
            "height": h,
        }
    )

    img = np.array(screenshot)

    gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    if fx != 1 or fy != 1:
        gray = cv2.resize(gray, None, fx=fx, fy=fy, interpolation=cv2.INTER_CUBIC)

    _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    config = f"--oem 3 --psm {psm}"

    if whitelist:
        config += f" -c tessedit_char_whitelist={whitelist}"

    text = pytesseract.image_to_string(gray, config=config).strip()

    return {
        "text": text,
    }


def clean_ocr_numbers(text):

    numbers = re.findall(r"\d+(?:\.\d+)?", text)
    return numbers


def clean_ocr_text(text):
    text = re.sub(r"[^A-Za-z0-9\s'&.,:\-\(\)]", " ", text)

    text = re.sub(r"[ \t]+", " ", text)

    lines = text.splitlines()

    cleaned_lines = []
    buffer = ""

    for line in lines:
        line = line.strip()

        if not line:
            continue

        letters = re.findall(r"[A-Za-z]", line)
        if len(letters) < 3:
            continue

        line = re.sub(r"\s+", " ", line)

        if buffer:
            if buffer[-1].islower() or line[0].islower() or len(buffer.split()) <= 2:
                buffer += " " + line
            else:
                cleaned_lines.append(buffer)
                buffer = line
        else:
            buffer = line

    if buffer:
        cleaned_lines.append(buffer)

    cleaned_text = "\n".join(cleaned_lines)
    cleaned_text = re.sub(r"\b([A-Za-z]+) s\b", r"\1's", cleaned_text)

    return cleaned_text.strip()
