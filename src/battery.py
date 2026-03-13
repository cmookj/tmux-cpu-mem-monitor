import argparse
from datetime import timedelta

import psutil


def _get_charging_status():
    """Get the battery charging status"""
    battery = psutil.sensors_battery()
    return battery.power_plugged


def get_battery_percent():
    """Display battery percentage"""
    if _get_charging_status():
        return "Charging"

    battery = round(psutil.sensors_battery().percent)
    return f"{battery}%"


def get_battery_time():
    """Display battery time remaining in hours and minutes"""
    if _get_charging_status():
        return "Charging"

    time_left = timedelta(seconds=psutil.sensors_battery().secsleft)
    print(time_left)
    return str(time_left).split(".")[0]


def get_battery_long():
    """Display the remaining battery amount in a human-readable format.

    Examples:
    - Charging
    - Out of battery
    - Battery is almost empty
    - Battery is running low
    - More than half full
    ...
    """
    if _get_charging_status():
        return "Charging"

    battery_status = {
        (100, 100): "Fully charged",
        (95, 99): "Almost full",
        (74, 94): "More than 3/4 full",
        (50, 74): "More than half full",
        (26, 49): "Less than half full",
        (6, 25): "Battery is running low",
        (2, 5): "Battery is almost empty",
        (1, 1): "I'm dying over here",
        (0, 0): "Out of battery",
    }

    for (low, high), status in battery_status.items():
        if low <= psutil.sensors_battery().percent <= high:
            return status


def _remap_range(value, low, high, remap_low, remap_high):
    """Remap the battery percentage into a whole number from remap_low up to remap_high"""
    return remap_low + (value - low) * (remap_high - remap_low) // (high - low)


def get_battery_compact():
    """Display battery percentage in a compact format"""

    # Battery icons in Unicode which are available in NerdFonts
    # Note that the icons for battery levels in charging is irregular.

    icon_discharging = [
        0x000F008E,  #   0%
        0x000F007A,  #  10%
        0x000F007B,  #  20%
        0x000F007C,  #  30%
        0x000F007D,  #  40%
        0x000F007E,  #  50%
        0x000F007F,  #  60%
        0x000F0080,  #  70%
        0x000F0081,  #  80%
        0x000F0082,  #  90%
        0x000F0079,  # 100%
    ]
    icon_charging = [
        0x000F089F,  #   0%
        0x000F089C,  #  10%
        0x000F0086,  #  20%
        0x000F0087,  #  30%
        0x000F0088,  #  40%
        0x000F089D,  #  50%
        0x000F0089,  #  60%
        0x000F089E,  #  70%
        0x000F008A,  #  80%
        0x000F008B,  #  90%
        0x000F0085,  # 100%
    ]

    battery_percentage = psutil.sensors_battery().percent
    level = battery_percentage // 10

    # Unicode characters for the battery indicator
    if _get_charging_status():
        battery_indicator = chr(icon_charging[level])
    else: # Discharging
        battery_indicator = chr(icon_discharging[level])

    return f"{battery_indicator}"


def get_battery_quarter():
    """Display battery percentage in a compact format"""

    # Battery icons in Unicode which are available in NerdFonts
    # Note that the icons for battery levels in charging is irregular.

    # Level    Discharging    Charging
    # -----    -----------    --------
    #   0%       000F008e     000F089F
    #  10%       000F007A     000F089C
    #  20%       000F007B     000F0086
    #  30%       000F007C     000F0087
    #  40%       000F007D     000F0088
    #  50%       000F007E     000F089D
    #  60%       000F007F     000F0089
    #  70%       000F0080     000F089E
    #  80%       000F0081     000F008A
    #  90%       000F0082     000F008B
    # 100%       000F0079     000F0085

    level = psutil.sensors_battery().percent // 10

    # Unicode characters for the battery indicator
    if _get_charging_status():
        if level == 0:
            battery_indicator = chr(0x000F089F)
        elif level == 1:
            battery_indicator = chr(0x000F089C)
        elif level == 2:
            battery_indicator = chr(0x000F0086)
        elif level == 3:
            battery_indicator = chr(0x000F0087)
        elif level == 4:
            battery_indicator = chr(0x000F0088)
        elif level == 5:
            battery_indicator = chr(0x000F089D)
        elif level == 6:
            battery_indicator = chr(0x000F0089)
        elif level == 7:
            battery_indicator = chr(0x000F089E)
        elif level == 8:
            battery_indicator = chr(0x000F008A)
        elif level == 9:
            battery_indicator = chr(0x000F008B)
        else:
            battery_indicator = chr(0x000F0085)
    else: # Discharging
        if level == 0:
            battery_indicator = chr(0x000F008e)
        elif level == 10:
            battery_indicator = chr(0x000F0079)
        else:
            battery_indicator = chr(0x000F0079 + level)

    return f"{battery_indicator}"


def main(args):
    if args.percent:
        battery = get_battery_percent()
    elif args.time:
        battery = get_battery_time()
    elif args.long:
        battery = get_battery_long()
    elif args.fun:
        battery = get_battery_long(mode="humor")
    elif args.compact:
        battery = get_battery_compact()
    elif args.quarter:
        battery = get_battery_quarter()
    else:
        battery = get_battery_percent()

    print(battery)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    type_option = parser.add_mutually_exclusive_group()
    type_option.add_argument(
        "-p",
        "--percent",
        action="store_true",
        default=False,
        help="display remaining battery percentage",
    )
    type_option.add_argument(
        "-t",
        "--time",
        action="store_true",
        default=False,
        help="display remaining battery time",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-l",
        "--long",
        action="store_true",
        default=False,
        help="display remaining battery as a sentence",
    )
    group.add_argument(
        "-f",
        "--fun",
        action="store_true",
        default=False,
        help="display remaining battery with humor",
    )
    parser.add_argument(
        "-c",
        "--compact",
        action="store_true",
        default=False,
        help="display remaining battery as an icon",
    )
    parser.add_argument(
        "-q",
        "--quarter",
        action="store_true",
        default=False,
        help="display remaining battery as a quarter-level icon",
    )
    args = parser.parse_args()
    main(args)
