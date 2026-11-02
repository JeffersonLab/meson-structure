#!/usr/bin/env python3
"""Command-line entry point for pion-neutron reconstruction."""

# Make analysis/common importable when run from this channel directory.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from reconstruction import main

if __name__ == "__main__":
    main()
