#!/usr/bin/python3.8

# This is a Python-based program created by Brandon Frostbourne for
# a Marymount University capstone project for the summer of 2020.
# See ../license.rst for MIT license.

# The goal of this program is to watch for any plugged in media through udev, then
# automate the bitstream process, securing the data in a secure file container using
# sfsimage, a shell script created by Bruce Nikkel. This image will then be analyzed using
# /tools/analysis.py to generate an html document in the specified folder where the sfs image resides,
# as well as in the read-only sfsimage.

# Standard Library Imports
import re
import sys

# Locally Developed Imports
from core.core import NorseTech as norse

# Third Party Imports
import pyudev


def main():
    config = {}
    while True:
        monitor_loop(config)


def monitor_loop(config: dict):

    context = pyudev.Context()
    minotaur = pyudev.Monitor.from_netlink(context)
    minotaur.filter_by(subsystem=['usb', 'block'])

    for device in iter(minotaur.poll, None):
        if device.action == 'add':
            try:
                maze = norse(config)
                maze.workhorse(device)
            except FileNotFoundError:
                print(f'Cannot find device or device does not exist.  Please try again later.')
                sys.exit(0)


if __name__ == "__main__":
    main()
