#!/usr/bin/env python3

import sys

CLIMA_POWER_STEP = 0.5
PASSIVE_STEP = 0.25


def parse_thresholds(argv):
    if len(argv) != 3:
        sys.exit("Usage: python expert_system.py <heating_below> <cooling_above>")
    try:
        low, high = float(argv[1]), float(argv[2])
    except ValueError:
        sys.exit("Thresholds must be numbers")
    if low >= high:
        sys.exit("First threshold must be lower than the second")
    return low, high


def choose_action(action, indoor, low, high, mid):
    if action == "heating":
        return "heating" if indoor < mid else "nothing"
    if action == "cooling":
        return "cooling" if indoor > mid else "nothing"
    if indoor < low:
        return "heating"
    if indoor >= high:
        return "cooling"
    return "nothing"


def update_temperature(indoor, outside, action, previous_action, diff_temp):
    if action != previous_action and action != "nothing":
        diff_temp = indoor - outside

    if action == "heating":
        diff_temp += CLIMA_POWER_STEP
        indoor = outside + diff_temp
    elif action == "cooling":
        diff_temp -= CLIMA_POWER_STEP
        indoor = outside + diff_temp
    elif indoor < outside:
        indoor = min(indoor + PASSIVE_STEP, outside)
    elif indoor > outside:
        indoor = max(indoor - PASSIVE_STEP, outside)

    return indoor, diff_temp


def main():
    low, high = parse_thresholds(sys.argv)
    mid = (low + high) / 2
    indoor, action, diff_temp = None, "nothing", 0.0

    for line in sys.stdin:
        try:
            outside = float(line.strip())
        except ValueError:
            continue

        if indoor is None:
            indoor = outside

        new_action = choose_action(action, indoor, low, high, mid)
        indoor, diff_temp = update_temperature(
            indoor, outside, new_action, action, diff_temp
        )
        action = new_action

        print(f"{outside} - {action} - {round(indoor, 2)}", flush=True)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, BrokenPipeError):
        sys.exit(0)