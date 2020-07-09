#!/bin/python3.8

# Standard Library Imports
import asyncio

# Locally Developed Imports
from core.tools.analysis import *
from core.tools.bitstream import SecureCopy as sc

# Third Party Imports


class NorseTech:

    def __init__(self):
        self.diskinfo = []

    def __initsys(self):
        # Initialize the ignored disks.  I'm not sure if I should have this,
        # as the main OS disk should always be /dev/sda
        # Remove this later, once I figure out how to use udev to monitor files -> Monitor at the NorseTech level
        return 0

    def workhorse(self):
        # Do the thing
        # Note to self, core abstraction is designed to get to a point where this class does the full shebang from
        # start to finish, and NorseTech.py just calls this every time a new drive is added.  That means
        # that I need to put the disk detection monitor in the main file, or have it as a separate func in core
        return 0