
import time

SWITCH_PAGES = {
    0: "home",
    1: "news",
    2: "trains",
    3: "weather",
    4: "sensor",
    5: "lists",
    6: "settings",
    7: "games",
    8: "unused",
    9: "pi hole",
    10: "security",
    11: "keychain",
}

BUTTON_PAGES = {
    0: "home",       # Status
    1: "trains",     # Maps
    2: "lists",      # Archives
    3: "weather",    # Sensor
}

page_state = {
    "switch_page": "home",
    "current_page": "home",
}

override = None
last = None


def handle_button(button_value, switch_page):
    global override
    page = BUTTON_PAGES.get(button_value)
    if page is None:
        return
    page_state["current_page"] = page
    if switch_page == "home" or button_value == 0:
        override = None
    else:
        override = time.monotonic() + 30


def update_page(switch_value):
    global override, last
    switch_page = SWITCH_PAGES.get(switch_value)
    if switch_page is None:
        return page_state["current_page"]
    page_state["switch_page"] = switch_page
    if last is None:
        last = switch_page
    elif switch_page != last:
        page_state["current_page"] = switch_page
        override = None
        last = switch_page
        return page_state["current_page"]
    if override is not None:
        if time.monotonic() >= override:
            page_state["current_page"] = switch_page
            override = None
    return page_state["current_page"]
