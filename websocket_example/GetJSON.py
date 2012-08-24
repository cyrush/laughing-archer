import os
from visit import *
from convert_obj_three import convert_ascii, convert_binary
import json

def GetJSON(filebase="_stuff/visit", TYPE="ascii"):
    # Save the window as OBJ file format.
    swa = GetSaveWindowAttributes()
    swa.fileName = filebase
    swa.family = 0
    swa.format = swa.OBJ
    SetSaveWindowAttributes(swa)
    name = SaveWindow()

    # If there was a .visit file, get the contents of it.
    filenames = []
    s = os.stat(name)
    if s.st_size == 0:
        visitfile = name[:-4] + ".visit"
        try:
            s = os.stat(visitfile)
            filenames = [ x[:-1] for x in open(visitfile, "rt").readlines()[1:]]
        except OSError:
            pass
    else:
        filenames = [name]

    # Convert each of the files to JSON.
    jsons = []
    for f in filenames:
        outfile = f[:-4] + ".js"
        if TYPE == "ascii":
            morphfiles = ""
            colorfiles = ""
            convert_ascii(f, morphfiles, colorfiles, outfile)
        else:
            convert_binary(f, outfile)
        # Read the json back in
        cydumb = json.loads(open(outfile).read())
        jsons.append(cydumb)
    return jsons

# #####################################################
# Main
# #####################################################
if __name__ == "__main__":
    OpenDatabase("~/data/noise.silo")
    AddPlot("Pseudocolor", "hardyglobal")
    DrawPlots()

    jsons = GetJSON(filebase="testing", TYPE="ascii")
    print jsons
