#!/usr/bin/env python3

import sys
import math
import random
import time

SEASONS = {
    "spring": (15, 6),
    "summer": (25, 7),
    "autumn": (10, 5),
    "winter": (0, 4),
}

NOISE = 0.3
SLICE = 48
SHIFT_HOURS = 9

if len(sys.argv) != 2:
    print("Usage: python environment.py <season>", file=sys.stderr)
    sys.exit(1)

season = sys.argv[1].lower()

if season not in SEASONS:
    print("Invalid season", file=sys.stderr)
    sys.exit(1)

base, amplitude = SEASONS[season]
i = 0 #polnoc

try:
    while True:
        hour = i * 0.5
        temperature = base + amplitude * math.sin(2 * math.pi * (hour - SHIFT_HOURS) / 24)
        temperature += random.uniform(-NOISE, NOISE)
        print(round(temperature, 2), flush=True)
        i = (i + 1) % SLICE
        time.sleep(1)
except KeyboardInterrupt:
    sys.exit(0)
    
except BrokenPipeError:
    sys.exit(0)