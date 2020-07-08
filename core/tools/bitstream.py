#!/bin/python3.8

# Standard Library Imports
import os
import subprocess
from pathlib import Path
import asyncio
from datetime import datetime

# Locally Developed Imports

# Third Party Imports


class SecureCopy:

    def __init__(self):
        self.__loc = Path.cwd()

    async def media_copy(self, mloc: Path, floc: Path):
        """Bitstream copy media to target sfs container

        :param mloc: location of media drive.  ex: /dev/sdb
        :type mloc: Path
        :param floc: location of target destination.  ex: ~/tmp/destination.sfs
        :type floc: Path
        """
        try:
            copy = await asyncio.create_subprocess_exec(
                self.sfsiloc().absolute(),
                f"-i {mloc.absolute()} {floc.absolute()}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await copy.communicate()
        except Exception as err:
            print(f"Error: {err}")
            raise Exception

    def sfsiloc(self):
        """Provides the location for sfsimage as a Path
        """
        return Path(self.__loc / "core" / "external" / "sfsi" / "sfsimage")


