#!/bin/python3.8

# Standard Library Imports
import os, platform
from pathlib import Path

# Locally Developed Imports

# Third Party Imports


class Norsalysis:
    """The class to catalogue and analyze everything within a specific Path--recursively--, and produce a JSON or CSV file of the output.
    :param pathloc: Path to location of folder

    """

    def __init__(
            self,
            pathloc: Path,
            opstyle = "json"
    ):
        self.pathloc = pathloc
        self.opstyle = opstyle
        self.masterlist = {
            "Directories": [],
            "DCount": 0,
            "Files": [],
            "FCount": 0,
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

    def fileTyping(self, mlist: list):
        """Create a dictionary of all filetypes in a given list

        :param mlist: List of full paths to file.  ex: ["/ect/test.txt"]
        :type mlist: list
        :returns: dict -- dict of itemized filetypes; keys are filetypes, values are list of all files matching type
        :raises: Exception -- general exception
        """
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
            return typedict

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

    def __init__(self, cmd="smartctl", devloc=None):
        if not os.getuid() == 0:
            raise PermissionError
        self.__cmd = cmd
        self.devloc = devloc
        self.devinf = {}

    def __cmd_me(self, param):
        params = {
            "scan": f"{self.__cmd} --scan",
            "test": f"{self.__cmd} --test = short /dev/{self.devloc}",
            "standard": f"{self.__cmd} -{param} /dev/{self.devloc}"
        }

        if not param in params.keys():
            return params["standard"]
        else:
            return params[param]

    def dev_name_scl(self):
        getdata = os.popen(self.__cmd_me("scan"))
        splitdata = (getdata.read()).split(' ')

        tempsplit = splitdata[0].split('/')
        self.devloc = tempsplit[2]

    def dev_info_scl(self):
        getdata = os.popen(self.__cmd_me("i"))
        readdata = getdata.read().splitlines()

        for x in range(4, len(readdata) -1):
            lines = readdata[x]
            tempdata = lines.split(':')
            self.devinf[tempdata[0]] = tempdata[1]

    def dev_info_hdp(self):
        getdata = os.popen(self.__cmd_me("I"))