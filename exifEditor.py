import subprocess
import os
import re


def validate(imageDir):
    subprocess.Popen(["/bin/bash", "-c", "for f in {}/*.JPG; do exiftool -all= -tagsfromfile @ -all:all -unsafe -icc_profile $f; done".format(imageDir)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
    for f in os.listdir(imageDir):
        if re.search("^.*original$", f):
            os.remove(os.path.join(imageDir, f))
