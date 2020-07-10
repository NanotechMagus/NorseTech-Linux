#!/bin/python3.8

# Standard Library Imports
from pathlib import Path

# Locally Developed Imports
from core.tools.analysis import *
from core.tools.bitstream import SecureCopy as sc

# Third Party Imports
import asyncio


class NorseTech:

    def __init__(self, config: dict):
        self.diskinfo = []
        self.forloc = Path(config['forloc'])

    async def workhorse(self, devinfo):
        # Do the thing
        # Note to self, core abstraction is designed to get to a point where this class does the full shebang from
        # start to finish, and NorseTech.py just calls this every time a new drive is added.  That means
        # that I need to put the disk detection monitor in the main file, or have it as a separate func in core

        try:
            sleipnir = DeviceInfo()
            mimir = sc()
            parsedevinfo = asyncio.create_task(
                sleipnir.dev_info_parser(devinfo)
            )
            startbitstream = asyncio.create_task(
                mimir.media_copy(sleipnir.devloc, self.forloc)
            )

            await parsedevinfo
            done, pending = await asyncio.wait({startbitstream})
            if startbitstream in done:
                await mimir.mount_point()

            if mimir.mounted:
                analysis = Norsalysis(mimir.fmount)
                await analysis.WalkDirectory()
                await analysis.fileTyping()
                await mimir.umount_point()

        except Exception:
            parsedevinfo = None
            startbitstream = None

        return 0

