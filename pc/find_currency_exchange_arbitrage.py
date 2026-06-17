import pyautogui
from utility.text_from_image import (
    read_text_from_image,
    clean_ocr_text,
    clean_ocr_numbers,
)
from collections import defaultdict
from utility.config import REGIONS, STARTING_POSITIONS
from utility.focus_game import focus_game
import re
import os
import shutil
from collections import defaultdict

pyautogui.PAUSE = 0


def open_currency_tab(tab_name):
    pyautogui.moveTo(
        STARTING_POSITIONS["npcs"]["ange"]["currency_exchange"]["tabs"][tab_name]
    )
    pyautogui.sleep(0.2)
    pyautogui.click()
    pyautogui.sleep(0.05)

    return True


def modify_currency_name(currency_name):
    modified_currency_name = None

    # edge cases
    if re.search(r"Support\s+Gem", currency_name):
        modified_currency_name = "creates a support\\sgem "

    elif re.search(r"Skill\s+Gem", currency_name):
        modified_currency_name = "a\\sskill gem "

    elif re.search(r"Spirit\s+Gem", currency_name):
        modified_currency_name = "persistent\\sskill gem "

    if modified_currency_name:
        level_match = re.search(r"level\s*(\d+)", currency_name, re.IGNORECASE)

        if level_match:
            modified_currency_name = modified_currency_name + level_match.group(1)

        return modified_currency_name

    return "^" + re.escape(currency_name).replace(r"\ ", r"\s") + "$"


def get_tab_currency_names():
    starting_region = REGIONS["npcs"]["ange"]["currency_exchange"]["tab_currency_text"]
    region_width = starting_region[2]
    region_height = starting_region[3]
    region_offset_x = 225
    region_offset_y = 48
    rows = 4
    cols = 3

    popular_currency_names = []

    for i in range(0, cols):
        for j in range(0, rows):
            region = (
                starting_region[0] + region_offset_x * i,
                starting_region[1] + region_offset_y * j,
                region_width,
                region_height,
            )
            res = read_text_from_image(region=region)

            if not res:
                continue

            currency_name = clean_ocr_text(res["text"])
            popular_currency_names.append(currency_name)

    return popular_currency_names


def get_market_ratio():
    res = read_text_from_image(
        region=REGIONS["npcs"]["ange"]["currency_exchange"]["market_ratio"],
        psm=7,
        fx=6,
        fy=6,
        whitelist="0123456789.:",
    )

    if res:
        market_ratio = clean_ocr_numbers(res["text"])
        return market_ratio

    return None


def open_currency_side(side_type):
    pyautogui.moveTo(STARTING_POSITIONS["npcs"]["ange"]["currency_exchange"][side_type])
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.3)


def find_currency_in_currency_exchange(currency_name):
    print(f"finding {currency_name} in currency exchange...$")
    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.02)
    pyautogui.press("f")
    pyautogui.sleep(0.02)
    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.05)
    pyautogui.typewrite(currency_name)
    pyautogui.sleep(0.25)

    pyautogui.moveTo(
        STARTING_POSITIONS["npcs"]["ange"]["currency_exchange"]["found_currency"]
    )
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.5)

    return True


def switch_currency_side_type():
    pyautogui.moveTo(STARTING_POSITIONS["npcs"]["ange"]["currency_exchange"]["i_want"])
    pyautogui.sleep(0.02)
    pyautogui.keyDown("ctrl")
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.02)
    pyautogui.keyUp("ctrl")
    pyautogui.sleep(0.05)


def close_search_page():
    pyautogui.moveTo(
        STARTING_POSITIONS["npcs"]["ange"]["currency_exchange"]["search_x_button"]
    )
    pyautogui.sleep(0.02)
    pyautogui.click()
    pyautogui.sleep(0.1)


def normalize_currency_name(name):
    return name.lower().replace("\\s+", " ").strip()


def create_patient_sale_arbitrage_opportunities(
    currency_prices,
    file_name="patient_arbitrage_opportunities.txt",
    destination_folder="logs/arbitrage",
):
    direct_rates = defaultdict(dict)

    for row in currency_prices:
        i_want = row.get("i_want")
        i_have = row.get("i_have")
        market_ratio = row.get("market_ratio")

        if not i_want or not i_have or market_ratio is None:
            continue

        try:
            market_ratio = float(market_ratio)
        except (TypeError, ValueError):
            continue

        if market_ratio <= 0:
            continue

        source = i_want
        target = i_have
        effective_rate = 1.0 / market_ratio

        current_best = direct_rates[source].get(target, 0.0)

        if effective_rate > current_best:
            direct_rates[source][target] = effective_rate

    opportunities = []
    seen_cycles = set()

    currencies = list(direct_rates.keys())

    for start in currencies:

        for mid, rate1 in direct_rates.get(start, {}).items():

            if mid == start:
                continue

            for end, rate2 in direct_rates.get(mid, {}).items():

                if end in (start, mid):
                    continue

                rate3 = direct_rates.get(end, {}).get(start)

                if rate3 is None:
                    continue

                final_amount = rate1 * rate2 * rate3

                if final_amount <= 1.0:
                    continue

                profit = final_amount - 1.0
                roi = profit

                cycle_key = tuple(sorted([start, mid, end]))

                if cycle_key in seen_cycles:
                    continue

                seen_cycles.add(cycle_key)

                opportunities.append(
                    {
                        "roi": roi,
                        "profit": profit,
                        "start_currency": start,
                        "mid_currency": mid,
                        "end_currency": end,
                        "rate1": rate1,
                        "rate2": rate2,
                        "rate3": rate3,
                        "final_amount": final_amount,
                    }
                )

    opportunities.sort(
        key=lambda x: (x["roi"], x["profit"]),
        reverse=True,
    )

    lines = []

    for op in opportunities:

        line = (
            f"ROI: {op['roi']:.2%}\n"
            f"PROFIT: {op['profit']:.4f} {op['start_currency']}\n"
            f"PATH:\n"
            f"\t- {op['start_currency']} -> {op['mid_currency']} "
            f"(1 {op['start_currency']} -> "
            f"{op['rate1']:.6f} {op['mid_currency']})\n"
            f"\t- {op['mid_currency']} -> {op['end_currency']} "
            f"(1 {op['mid_currency']} -> "
            f"{op['rate2']:.6f} {op['end_currency']})\n"
            f"\t- {op['end_currency']} -> {op['start_currency']} "
            f"(1 {op['end_currency']} -> "
            f"{op['rate3']:.6f} {op['start_currency']})\n"
        )

        lines.append(line)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines))

    shutil.move(file_name, os.path.join(destination_folder, file_name))

    return lines


def create_instant_sale_arbitrage_opportunities(
    currency_prices,
    file_name="instant_sale_arbitrage_opportunities.txt",
    destination_folder="logs/arbitrage",
):

    direct_rates = defaultdict(dict)

    for row in currency_prices:

        i_want = row.get("i_want")
        i_have = row.get("i_have")
        market_ratio = row.get("market_ratio")

        if not i_want or not i_have or market_ratio is None:
            continue

        try:
            market_ratio = float(market_ratio)
        except (TypeError, ValueError):
            continue

        if market_ratio <= 0:
            continue
        source = i_have
        target = i_want
        effective_rate = market_ratio

        current_best = direct_rates[source].get(target)

        if current_best is None or effective_rate < current_best:
            direct_rates[source][target] = effective_rate

    opportunities = []
    seen_cycles = set()

    currencies = list(direct_rates.keys())

    for start in currencies:

        for mid, rate1 in direct_rates.get(start, {}).items():

            if mid == start:
                continue

            for end, rate2 in direct_rates.get(mid, {}).items():

                if end in (start, mid):
                    continue

                rate3 = direct_rates.get(end, {}).get(start)

                if rate3 is None:
                    continue

                final_amount = rate1 * rate2 * rate3

                if final_amount <= 1.0:
                    continue

                profit = final_amount - 1.0
                roi = profit

                cycle_key = tuple(sorted([start, mid, end]))

                if cycle_key in seen_cycles:
                    continue

                seen_cycles.add(cycle_key)

                opportunities.append(
                    {
                        "roi": roi,
                        "profit": profit,
                        "start_currency": start,
                        "mid_currency": mid,
                        "end_currency": end,
                        "rate1": rate1,
                        "rate2": rate2,
                        "rate3": rate3,
                        "final_amount": final_amount,
                    }
                )

    opportunities.sort(
        key=lambda x: (x["roi"], x["profit"]),
        reverse=True,
    )

    lines = []

    for op in opportunities:

        line = (
            f"ROI: {op['roi']:.2%}\n"
            f"PROFIT: {op['profit']:.4f} {op['start_currency']}\n"
            f"PATH:\n"
            f"\t- instant convert "
            f"{op['start_currency']} -> {op['mid_currency']} "
            f"(1 {op['start_currency']} -> "
            f"{op['rate1']:.6f} {op['mid_currency']})\n"
            f"\t- instant convert "
            f"{op['mid_currency']} -> {op['end_currency']} "
            f"(1 {op['mid_currency']} -> "
            f"{op['rate2']:.6f} {op['end_currency']})\n"
            f"\t- instant convert "
            f"{op['end_currency']} -> {op['start_currency']} "
            f"(1 {op['end_currency']} -> "
            f"{op['rate3']:.6f} {op['start_currency']})\n"
        )

        lines.append(line)

    with open(file_name, "w", encoding="utf-8") as f:
        f.write("\n\n".join(lines))

    shutil.move(file_name, os.path.join(destination_folder, file_name))

    return lines


def get_tab_currency_names_for_main_currencies(
    main_currency_names, tab_name, main_side_type, secondary_side_type
):
    popular_currency_names = set()

    for main_currency_name in main_currency_names:
        modified_main_currency_name = (
            "^" + re.escape(main_currency_name).replace(r"\ ", r"\s") + "$"
        )

        open_currency_side(side_type=main_side_type)

        find_currency_in_currency_exchange(currency_name=modified_main_currency_name)

        open_currency_side(side_type=secondary_side_type)
        pyautogui.sleep(
            0.25
        )  # edge case as sometimes tab loads slower and I am too lazy to wait for tab to load
        open_currency_tab(tab_name=tab_name)

        tab_currency_names = get_tab_currency_names()

        if not tab_currency_names:
            continue

        close_search_page()

        popular_currency_names.update(tab_currency_names)

    return popular_currency_names


def find_currency_exchange_arbitrage():
    popular_currency_prices = []
    main_currency_names = ["Exalted Orb", "Chaos Orb"]
    popular_currency_names = set(
        [
            "Armourer's Scrap",
            "Blacksmith's Whetstone",
            "Greater Jeweller's Orb",
            "Perfect Jeweller's Orb",
            "Vaal Orb",
            "Orb of Alchemy",
            "Regal Orb",
            "Artificer's Orb",
            "Gemcutter's Prism",
            "Orb of Annulment",
        ]
    )
    main_side_type = "i_have"
    secondary_side_type = "i_want"
    tab_name = "popular"

    tab_currency_names = get_tab_currency_names_for_main_currencies(
        main_currency_names=main_currency_names,
        tab_name=tab_name,
        main_side_type=main_side_type,
        secondary_side_type=secondary_side_type,
    )

    popular_currency_names.update(tab_currency_names)

    for main_currency_name in main_currency_names:
        modified_main_currency_name = (
            "^" + re.escape(main_currency_name).replace(r"\ ", r"\s") + "$"
        )

        open_currency_side(side_type=main_side_type)
        find_currency_in_currency_exchange(currency_name=modified_main_currency_name)
        open_currency_side(side_type=secondary_side_type)
        tab_open = True

        for popular_currency_name in popular_currency_names:

            if main_currency_name.lower() == popular_currency_name.lower():
                continue

            modified_popular_currency_name = modify_currency_name(
                currency_name=popular_currency_name
            )

            print("main_currency_name: ", popular_currency_name)
            print("modified_main_currency_name: ", modified_popular_currency_name)

            if not tab_open:
                open_currency_side(side_type=secondary_side_type)

            i_want_currency_res = find_currency_in_currency_exchange(
                currency_name=modified_popular_currency_name
            )
            tab_open = False

            if not i_want_currency_res:
                print("unable to find i want currency...")
                return None

            market_ratio_res_one = get_market_ratio()

            if len(market_ratio_res_one) < 2:
                continue

            market_ratio_one = float(market_ratio_res_one[0]) / float(
                market_ratio_res_one[1]
            )

            switch_currency_side_type()

            market_ratio_res_two = get_market_ratio()

            if len(market_ratio_res_two) < 2:
                switch_currency_side_type()
                continue

            market_ratio_two = float(market_ratio_res_two[0]) / float(
                market_ratio_res_two[1]
            )
            popular_currency_prices.append(
                {
                    "i_want": popular_currency_name,
                    "i_have": main_currency_name,
                    "market_ratio": market_ratio_one,
                }
            )
            popular_currency_prices.append(
                {
                    "i_want": main_currency_name,
                    "i_have": popular_currency_name,
                    "market_ratio": market_ratio_two,
                },
            )

            print(
                {
                    "i_want": popular_currency_name,
                    "i_have": main_currency_name,
                    "market_ratio": market_ratio_one,
                },
                {
                    "i_want": main_currency_name,
                    "i_have": popular_currency_name,
                    "market_ratio": market_ratio_two,
                },
            )
            switch_currency_side_type()

    print(popular_currency_prices)
    create_instant_sale_arbitrage_opportunities(currency_prices=popular_currency_prices)
    create_patient_sale_arbitrage_opportunities(currency_prices=popular_currency_prices)


find_currency_exchange_arbitrage()
# create_instant_sale_arbitrage_opportunities(
#     currency_prices=[
#         {"i_want": "Exalted Orb", "i_have": "Chaos Orb", "market_ratio": 5},
#         {"i_want": "Chaos Orb", "i_have": "Exalted Orb", "market_ratio": 0.1428},
#         {"i_want": "Vaal Orb", "i_have": "Exalted Orb", "market_ratio": 2},
#         {"i_want": "Exalted Orb", "i_have": "Vaal Orb", "market_ratio": 0.333},
#         {"i_want": "Vaal Orb", "i_have": "Chaos Orb", "market_ratio": 5},
#         {"i_want": "Chaos Orb", "i_have": "Vaal Orb", "market_ratio": 0.1428},
#     ]
# )
# create_patient_sale_arbitrage_opportunities(
#     currency_prices=[
#         {"i_want": "Exalted Orb", "i_have": "Chaos Orb", "market_ratio": 5},
#         {"i_want": "Chaos Orb", "i_have": "Exalted Orb", "market_ratio": 0.1428},
#         {"i_want": "Vaal Orb", "i_have": "Exalted Orb", "market_ratio": 2},
#         {"i_want": "Exalted Orb", "i_have": "Vaal Orb", "market_ratio": 0.333},
#         {"i_want": "Vaal Orb", "i_have": "Chaos Orb", "market_ratio": 5},
#         {"i_want": "Chaos Orb", "i_have": "Vaal Orb", "market_ratio": 0.1428},
#     ]
# )

# find_currency_in_currency_exchange(currency_name="Uncut Support Gem (Level 5)")
# print(get_market_ratio())
# fix arbitrage algo
