#!/bin/python3.8

# Standard Library Imports
import os
import re
from pathlib import Path

# Locally Developed Imports

# Third Party Imports


class Norsalysis:
    """The class to catalogue and analyze everything within a specific Path--recursively--, and produce a JSON or CSV file of the output.
    :param pathloc: Path to location of folder

    """

    def __init__(self, pathloc: Path):
        self.pathloc = pathloc
        self.masterlist = {
            "Directories": [],
            "DCount": 0,
            "Files": [],
            "FCount": 0,
            "FileTyping": {},
            "Full List": {}
        }

    def WalkDirectory(self):
        """Discover all files and directories in folder

        :param folder: Path to location of folder.  ex: /tmp/mount
        :type folder: Path
        :returns: dict -- directory of all files and directories,
        :key: "Directories" -- list of all directories found in param
        :key: "DCount" -- int count of all directories
        :key: "Files" -- list of all files found in param
        :key: "FCount" -- int count of all files
        :key: "Full List" -- dict of all files and directories (may be phased out)
        :raises: Exception -- general exception
        """

        try:
            for root, directories, files in os.walk(str(self.pathloc)):
                self.masterlist["Full List"][root] = {
                    "Files": []
                }
                for d in directories:
                    dplus = str((Path(root) / d).absolute())
                    self.masterlist["Full List"][dplus] = {
                        "Files": []
                    }
                    self.masterlist["Directories"].append(dplus)
                    print(f"Folders : {dplus}")
                for f in files:
                    fplus = str((Path(root) / f).absolute())
                    self.masterlist["Full List"][str(root)]["Files"].append(str(f))
                    self.masterlist["Files"].append(fplus)
                    print(f"Files   : {fplus}")
        except Exception as err:
            print(f"Error: {err}")
            raise Exception
        finally:
            self.__countUpdate("f")
            self.__countUpdate("d")
            return self.masterlist

    def fileTyping(self, mlist=None):
        """Create a dictionary of all filetypes in a given list

        :param mlist: List of full paths to file.  ex: ["/ect/test.txt"]
        :type mlist: list
        :returns: dict -- dict of itemized filetypes; keys are filetypes, values are list of all files matching type
        :raises: Exception -- general exception
        """
        if not mlist:
            mlist = self.masterlist['Files']

        typedict = {}

        try:
            for x in mlist:
                splitthis = os.path.splitext(x)
                filetypethis = str(splitthis[1])[1:]
                if not typedict.get(filetypethis, None):
                    typedict[filetypethis] = []
                elif filetypethis == "" or not filetypethis:
                    filetypethis = "No filetype"
                    typedict[filetypethis] = []
                typedict[filetypethis].append(str(x))
        except Exception as err:
            print(f"Error: {err}")
        finally:
            self.masterlist["Filetyping"] = typedict

    def __countUpdate(self, ftype: str):
        """Updates the FCount or DCount value in self.masterlist
        Note: Private function, scope not available outside class.

        :param ftype: 'f' or 'd' for files or directories respectively"""
        ccheck = {
            "d": ["DCount", "Directories"],
            "f": ["FCount", "Files"]
        }

        self.masterlist[ccheck[ftype][0]] = len(self.masterlist[ccheck[ftype][1]])
        return

    def __jsonconv(self, conv: dict):
        import json
        return json.dumps(conv)


class DeviceInfo:
    #TODO: Write Documentation for this class

    def __init__(self):
        if not os.getuid() == 0:
            raise PermissionError
        self.devloc = None
        self.devinf = {}

    def dev_info_scl(self):
        readdata = self.dev_getdata("smartctl", "-i")

        for x in range(4, len(readdata) -1):
            lines = readdata[x]
            tempdata = lines.split(':')
            self.devinf[tempdata[0]] = tempdata[1]

    def dev_usb_info(self, devusb):
        # Take BUS:Device location, update initial drive information
        drakken = re.compile(r'sd.')
        party = re.compile(r':')
        try:
            readdata = self.dev_getdata("lsusb", f"-v -s {devusb}")

            for x in range(len(readdata)):
                lines = readdata[x]
                if party.search(lines):
                    tempdata = lines.split(':')
                    self.devinf["USBInfo"][tempdata[0]] = tempdata[1]
                    if drakken.search(tempdata[1]):
                        self.devloc = drakken.search(tempdata[1])
        except FileNotFoundError as err:
            print(f'Error! {err}')

    def dev_block_info(self, devblock):
        # Take block address, update drive information
        party = re.compile(r':')
        try:
            self.devloc = f"/dev/{devblock}"
            readdata = self.dev_getdata("lsblk", f"-O {self.devloc}")

            for x in range(len(readdata)):
                lines = readdata[x]
                if party.search(lines):
                    tempdata = lines.split(':')
                    self.devinf["BlockInfo"][tempdata[0]] = tempdata[1]
        except FileNotFoundError as err:
            print(f'Error! {err}')

    def dev_getdata(self, cmd, params):
        if not self.devloc:
            getdata = os.popen(f"{cmd} {params}")
        else:
            getdata = os.popen(f"{cmd} {params} {self.devloc}")
        return getdata.read().splitlines()

    def dev_info_parser(self, devinfo):
        maze = {
            "usb": self.dev_usb_info,
            "sd.": self.dev_block_info
        }
        labyrinth = re.compile(r'usb\d|sd.')
        minotaur = RegexDict(maze)
        bull = labyrinth.search(devinfo)

        for axe in minotaur.get_matching(bull):
            if bull == "usb":
                lunrex = re.compile(r'\d:\d')
                axe(lunrex.search(devinfo))
            else:
                axe(bull)


class RegexDict(dict):

    def get_matching(self, event):
        return (self[key] for key in self if re.match(key, event))


class NorseLogistics():

    def __init__(self):
        self.initiate = None