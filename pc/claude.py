import pyautogui
from utility.text_from_image import (
    read_text_from_image,
    clean_ocr_text,
    clean_ocr_numbers,
)
from utility.config import REGIONS, STARTING_POSITIONS
import re

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
    pyautogui.sleep(0.2)

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
    output_file="patient_arbitrage_opportunities.txt",
):
    """
    Finds profitable arbitrage opportunities using patient trading:
    - Buy at the BEST (lowest) price across all offers
    - Sell at the BEST (highest) price across all offers
    
    This requires placing orders and waiting for them to fill.
    
    Data format:
    {'i_want': 'Greater Exalted Orb', 'i_have': "Exalted Orb", 'market_ratio': 0.1}
    Means: To buy 1 Greater Exalted Orb costs 1/0.1 = 10 Exalted Orbs
    Means: Selling 1 Greater Exalted Orb gets you 1/0.1 = 10 Exalted Orbs
    
    For BUYING an item (patient):
    - Find all entries where i_want == item
    - LOWEST (1/market_ratio) = cheapest way to buy that item
    
    For SELLING an item (patient):
    - Find all entries where i_have == item  
    - HIGHEST (1/market_ratio) = best return when selling that item
    
    Returns:
        List[str]: Human-readable arbitrage opportunities
    """
    from collections import defaultdict

    # best_buy_prices[item][currency] = lowest cost (in currency units) to buy 1 item
    best_buy_prices = defaultdict(dict)
    
    # best_sell_prices[item][currency] = highest revenue (in currency units) from selling 1 item
    best_sell_prices = defaultdict(dict)

    for row in currency_prices:
        i_want = row.get("i_want")
        i_have = row.get("i_have")
        ratio = row.get("market_ratio")

        if not i_want or not i_have or ratio is None:
            continue

        ratio = float(ratio)
        if ratio <= 0:
            continue

        # market_ratio is the direct exchange rate - use it as-is
        buy_cost = ratio
        
        # Track lowest buy cost (best patient buy price)
        if i_want not in best_buy_prices or i_have not in best_buy_prices[i_want]:
            best_buy_prices[i_want][i_have] = buy_cost
        else:
            best_buy_prices[i_want][i_have] = min(best_buy_prices[i_want][i_have], buy_cost)
        
        # Same market_ratio for selling (data has both directions already)
        sell_revenue = ratio
        
        # Track highest sell revenue (best patient sell price)
        if i_have not in best_sell_prices or i_want not in best_sell_prices[i_have]:
            best_sell_prices[i_have][i_want] = sell_revenue
        else:
            best_sell_prices[i_have][i_want] = max(best_sell_prices[i_have][i_want], sell_revenue)

    opportunities = []

    # Find all items that can be both bought and sold
    all_items = set(best_buy_prices.keys()) & set(best_sell_prices.keys())

    for item in all_items:
        buy_options = best_buy_prices[item]  # currencies we can use to buy this item
        sell_options = best_sell_prices[item]  # currencies we can get when selling this item

        for buy_currency, buy_cost in buy_options.items():
            for sell_currency, sell_revenue in sell_options.items():
                
                if buy_currency == sell_currency:
                    continue

                # Convert sell_revenue from sell_currency to buy_currency
                # Look up: when selling 1 sell_currency, how much buy_currency do we get?
                # This is in best_sell_prices[sell_currency][buy_currency]
                
                conversion_rate = best_sell_prices.get(sell_currency, {}).get(buy_currency)
                
                if conversion_rate is None:
                    continue

                # sell_revenue is in sell_currency
                # conversion_rate tells us how much buy_currency we get per 1 sell_currency
                # So: multiply them together
                revenue_in_buy_currency = sell_revenue * conversion_rate
                
                profit_in_buy_currency = revenue_in_buy_currency - buy_cost
                
                if profit_in_buy_currency <= 0:
                    continue

                roi = (profit_in_buy_currency / buy_cost) * 100

                opportunities.append({
                    "roi": roi,
                    "item": item,
                    "buy_currency": buy_currency,
                    "sell_currency": sell_currency,
                    "buy_cost": buy_cost,
                    "sell_revenue": sell_revenue,
                    "conversion_rate": conversion_rate,
                    "profit": profit_in_buy_currency,
                })

    opportunities.sort(key=lambda x: (x["roi"], x["profit"]), reverse=True)

    lines = []
    lines.append("=" * 80)
    lines.append("PATIENT SALE ARBITRAGE OPPORTUNITIES")
    lines.append("(Buy at best patient price, sell at best patient price)")
    lines.append("=" * 80)
    lines.append("")

    if not opportunities:
        lines.append("No profitable arbitrage opportunities found.")
    else:
        for i, op in enumerate(opportunities, 1):
            lines.append(f"\n--- Opportunity #{i} ---")
            lines.append(f"ROI: {op['roi']:.2f}%")
            lines.append(f"PROFIT: {op['profit']:.4f} {op['buy_currency']}")
            lines.append(f"ITEM: {op['item']}")
            lines.append(f"PATH:")
            lines.append(f"  1. Buy {op['item']} with {op['buy_currency']}")
            lines.append(f"     Cost: {op['buy_cost']:.4f} {op['buy_currency']}")
            lines.append(f"  2. Sell {op['item']} for {op['sell_currency']}")
            lines.append(f"     Revenue: {op['sell_revenue']:.4f} {op['sell_currency']}")
            lines.append(f"  3. Convert {op['sell_currency']} to {op['buy_currency']}")
            lines.append(f"     Rate: 1 {op['buy_currency']} = {op['conversion_rate']:.4f} {op['sell_currency']}")
            lines.append(f"     Final revenue: {op['sell_revenue'] / op['conversion_rate']:.4f} {op['buy_currency']}")
            lines.append("")

    output_text = "\n".join(lines)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)
    
    print(f"\n✓ Patient sale opportunities saved to: {output_file}")
    print(f"  Found {len(opportunities)} opportunities")
    
    return lines


def create_instant_sale_arbitrage_opportunities(
    currency_prices,
    output_file="instant_arbitrage_opportunities.txt",
):
    """
    Finds instant arbitrage opportunities:
    - Buy at market price (instant = HIGHEST asking price from sellers)
    - Sell at market price (instant = LOWEST bid price from buyers)
    
    Data format:
    {'i_want': 'Greater Exalted Orb', 'i_have': "Exalted Orb", 'market_ratio': 0.1}
    Means: To instant buy 1 Greater Exalted Orb costs 1/0.1 = 10 Exalted Orbs
    
    For INSTANT BUY an item:
    - Find all entries where i_want == item
    - HIGHEST (1/market_ratio) = worst case / most expensive instant buy price
    
    For INSTANT SELL an item:
    - Find all entries where i_have == item
    - LOWEST (1/market_ratio) = worst case / lowest instant sell price
    
    Returns:
        List[str]: Human-readable arbitrage opportunities
    """
    from collections import defaultdict

    # instant_buy_prices[item][currency] = highest cost (worst/most expensive instant buy)
    instant_buy_prices = defaultdict(dict)
    
    # instant_sell_prices[item][currency] = lowest revenue (worst/lowest instant sell)
    instant_sell_prices = defaultdict(dict)

    for row in currency_prices:
        i_want = row.get("i_want")
        i_have = row.get("i_have")
        ratio = row.get("market_ratio")

        if not i_want or not i_have or ratio is None:
            continue

        ratio = float(ratio)
        if ratio <= 0:
            continue

        # market_ratio is the direct exchange rate - use it as-is
        buy_cost = ratio
        
        # Track highest instant buy cost (worst price to instantly buy)
        if i_want not in instant_buy_prices or i_have not in instant_buy_prices[i_want]:
            instant_buy_prices[i_want][i_have] = buy_cost
        else:
            instant_buy_prices[i_want][i_have] = max(instant_buy_prices[i_want][i_have], buy_cost)
        
        # Same market_ratio for selling (data has both directions already)
        sell_revenue = ratio
        
        # Track lowest instant sell revenue (worst price to instantly sell)
        if i_have not in instant_sell_prices or i_want not in instant_sell_prices[i_have]:
            instant_sell_prices[i_have][i_want] = sell_revenue
        else:
            instant_sell_prices[i_have][i_want] = min(instant_sell_prices[i_have][i_want], sell_revenue)

    opportunities = []

    all_items = set(instant_buy_prices.keys()) & set(instant_sell_prices.keys())

    for item in all_items:
        buy_options = instant_buy_prices[item]
        sell_options = instant_sell_prices[item]

        for buy_currency, buy_cost in buy_options.items():
            for sell_currency, sell_revenue in sell_options.items():
                
                if buy_currency == sell_currency:
                    continue

                # Convert sell_revenue from sell_currency to buy_currency
                # Look up: when selling 1 sell_currency, how much buy_currency do we get?
                # This is in instant_sell_prices[sell_currency][buy_currency]
                conversion_rate = instant_sell_prices.get(sell_currency, {}).get(buy_currency)
                
                if conversion_rate is None:
                    continue

                # sell_revenue is in sell_currency
                # conversion_rate tells us how much buy_currency we get per 1 sell_currency
                # So: multiply them together
                revenue_in_buy_currency = sell_revenue * conversion_rate
                profit_in_buy_currency = revenue_in_buy_currency - buy_cost
                
                if profit_in_buy_currency <= 0:
                    continue

                roi = (profit_in_buy_currency / buy_cost) * 100

                opportunities.append({
                    "roi": roi,
                    "item": item,
                    "buy_currency": buy_currency,
                    "sell_currency": sell_currency,
                    "buy_cost": buy_cost,
                    "sell_revenue": sell_revenue,
                    "conversion_rate": conversion_rate,
                    "profit": profit_in_buy_currency,
                })

    opportunities.sort(key=lambda x: (x["roi"], x["profit"]), reverse=True)

    lines = []
    lines.append("=" * 80)
    lines.append("INSTANT SALE ARBITRAGE OPPORTUNITIES")
    lines.append("(Buy at worst instant price, sell at worst instant price)")
    lines.append("=" * 80)
    lines.append("")

    if not opportunities:
        lines.append("No profitable instant arbitrage opportunities found.")
    else:
        for i, op in enumerate(opportunities, 1):
            lines.append(f"\n--- Opportunity #{i} ---")
            lines.append(f"ROI: {op['roi']:.2f}%")
            lines.append(f"PROFIT: {op['profit']:.4f} {op['buy_currency']}")
            lines.append(f"ITEM: {op['item']}")
            lines.append(f"PATH:")
            lines.append(f"  1. Instant buy {op['item']} with {op['buy_currency']}")
            lines.append(f"     Cost: {op['buy_cost']:.4f} {op['buy_currency']}")
            lines.append(f"  2. Instant sell {op['item']} for {op['sell_currency']}")
            lines.append(f"     Revenue: {op['sell_revenue']:.4f} {op['sell_currency']}")
            lines.append(f"  3. Convert {op['sell_currency']} to {op['buy_currency']}")
            lines.append(f"     Rate: 1 {op['buy_currency']} = {op['conversion_rate']:.4f} {op['sell_currency']}")
            lines.append(f"     Final revenue: {op['sell_revenue'] / op['conversion_rate']:.4f} {op['buy_currency']}")
            lines.append("")

    output_text = "\n".join(lines)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(output_text)
    
    print(f"\n✓ Instant sale opportunities saved to: {output_file}")
    print(f"  Found {len(opportunities)} opportunities")
    
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
    popular_currency_names = set(["Armourer's Scrap", "Blacksmith's Whetstone"])
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
            switch_currency_side_type()

    print("\n" + "=" * 80)
    print(f"Collected {len(popular_currency_prices)} currency price entries")
    print("=" * 80)
    print(popular_currency_prices)
    
    create_instant_sale_arbitrage_opportunities(currency_prices=popular_currency_prices)
    create_patient_sale_arbitrage_opportunities(currency_prices=popular_currency_prices)


if __name__ == "__main__":
    find_currency_exchange_arbitrage()
