#!/usr/bin/env python3

import sys

STEP = 0.5
DRIFT = 0.25

if len(sys.argv) != 3:
    print("Usage: python expert_system.py <heating_below> <cooling_above>", file=sys.stderr)
    sys.exit(1)

try:
    low = float(sys.argv[1])
    high = float(sys.argv[2])
except ValueError:
    print("Thresholds must be numbers", file=sys.stderr)
    sys.exit(1)

if low >= high:
    print("First threshold must be lower than the second", file=sys.stderr)
    sys.exit(1)

mid = (low + high) / 2
indoor = None
action = "nothing"
offset = 0.0

try:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            outside = float(line)
        except ValueError:
            continue

        if indoor is None:
            indoor = outside

        if action == "heating":
            new_action = "heating" if indoor < mid else "nothing"
        elif action == "cooling":
            new_action = "cooling" if indoor > mid else "nothing"
        elif indoor < low:
            new_action = "heating"
        elif indoor >= high:
            new_action = "cooling"
        else:
            new_action = "nothing"

        if new_action != action and new_action != "nothing":
            offset = indoor - outside
        action = new_action

        if action == "heating":
            offset += STEP
            indoor = outside + offset
        elif action == "cooling":
            offset -= STEP
            indoor = outside + offset
        elif indoor < outside:
            indoor = min(indoor + DRIFT, outside)
        elif indoor > outside:
            indoor = max(indoor - DRIFT, outside)

        print(f"{outside} - {action} - {round(indoor, 2)}", flush=True)
except (KeyboardInterrupt, BrokenPipeError):
    sys.exit(0)