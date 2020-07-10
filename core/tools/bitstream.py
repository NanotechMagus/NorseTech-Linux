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
        self.sfsiloc = Path(self.__loc / "core" / "external" / "sfsi" / "sfsimage")
        self.floc = None
        self.fmount = None
        self.mounted = None

    async def media_copy(self, mloc: Path, floc: Path):
        """Bitstream copy media to target sfs container

        :param mloc: location of media drive.  ex: /dev/sdb
        :type mloc: Path
        :param floc: location of target destination.  ex: ~/tmp/destination.sfs
        :type floc: Path
        """
        try:
            timestamp = self.timestamp()
            copy = await asyncio.create_subprocess_exec(
                self.sfsiloc.absolute(),
                f"-i {mloc.absolute()} {floc.absolute()}/{timestamp}.sfs",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await copy.communicate()

            if stdout:
                print(f"[stdout]\n{stdout.decode()}")
            if stderr:
                print(f"[stderr]\n{stderr.decode()}")
            self.floc = Path(floc / str(timestamp))
            return
        except Exception as err:
            print(f"Error: {err}")
            raise Exception

    def timestamp(self):
        fmount = datetime.timestamp(datetime.now())
        return str(fmount)

    def mount_point(self):
        try:
            os.popen(f"{self.sfsiloc.absolute()} -m {self.floc.absolute()}.sfs {self.floc.absolute()}")
        except FileNotFoundError:
            return 0

    def umount_point(self):
        try:
            os.popen(f"{self.sfsiloc.absolute()} -u {self.floc.absolute()}")
        except FileNotFoundError:
            return 0