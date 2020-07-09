#!/bin/python3.8

# Standard Library Imports
from pathlib import Path

# Locally Developed Imports
from core.tools.analysis import *
from core.tools.bitstream import SecureCopy as sc

# Third Party Imports
import asyncio


class NorseTech:

    def __init__(self, devloc: str):
        self.diskinfo = []
        self.devloc = Path('/' + devloc)

    def workhorse(self):
        # Do the thing
        # Note to self, core abstraction is designed to get to a point where this class does the full shebang from
        # start to finish, and NorseTech.py just calls this every time a new drive is added.  That means
        # that I need to put the disk detection monitor in the main file, or have it as a separate func in core
        return 0

