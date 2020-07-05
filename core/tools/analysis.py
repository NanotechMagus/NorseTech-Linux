#!/bin/python3.8

# Standard Library Imports
import os
from pathlib import Path
import json

# Locally Developed Imports

# Third Party Imports


def WalkDirectory(folder):

    masterlist = {
        "Directories": [],
        "DCount": 0,
        "Files": [],
        "FCount": 0,
        "Full List": {}
    }
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
            masterlist["Files"].append(str(f))
            print(f"Files   : {fplus}")
    return json.dumps(masterlist, indent=2)