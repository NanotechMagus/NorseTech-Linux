#!/bin/python3.8

# Standard Library Imports
import os
from pathlib import Path
import json

# Locally Developed Imports

# Third Party Imports


def WalkDirectory(folder):
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
    masterlist = {
        "Directories": [],
        "DCount": 0,
        "Files": [],
        "FCount": 0,
        "Full List": {}
    }
    try:
        for root, directories, files in os.walk(folder):
            masterlist["Full List"][root] = {
                "Files": []
            }
            for d in directories:
                dplus = str((Path(root) / d).absolute())
                masterlist["Full List"][dplus] = {
                    "Files": []
                }
                masterlist["Directories"].append(dplus)
                print(f"Folders : {dplus}")
            for f in files:
                fplus = str((Path(root) / f).absolute())
                masterlist["Full List"][str(root)]["Files"].append(str(f))
                masterlist["Files"].append(fplus)
                print(f"Files   : {fplus}")
    except Exception as err:
        print(f"Error: {err}")
        raise Exception
    finally:
        masterlist["DCount"] = len(masterlist["Directories"])
        masterlist["FCount"] = len(masterlist["Files"])
        return masterlist


def fileTyping(mlist: list):
    """Create a dictionary of all filetypes in a given list

    :param mlist: List of full paths to file.  ex: ["/ect/test.txt"]
    :type mlist: list
    :returns: dict -- json string of itemized filetypes; keys are filetypes, values are list of all files matching type
    :raises: Exception -- general exception
    """
    typedict = {}
    try:
        for x in mlist:
            splitthis = os.path.splitext(x)
            filetypethis = str(splitthis[1])[1:]
            if not typedict.get(filetypethis, None):
                typedict[filetypethis] = []
            elif filetypethis == "":
                filetypethis = "No filetype"
                typedict[filetypethis] = []
            typedict[filetypethis].append(str(x))
    except Exception as err:
        print(f"Error: {err}")
    finally:
        return typedict