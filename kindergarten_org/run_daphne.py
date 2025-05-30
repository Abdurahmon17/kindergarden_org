# kindergarten_org/run_daphne.py
import eventlet
eventlet.monkey_patch()

import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from daphne.cli import CommandLineInterface

if __name__ == "__main__":
    CommandLineInterface().run(["kindergarten_org.asgi:application", "-b", "0.0.0.0", "-p", "8000"])