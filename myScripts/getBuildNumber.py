#!/usr/bin/env python

import sys
import os

sys.path.append(os.getcwd())
import operations

def usage():
    if len(sys.argv) > 1:
        main()
    else:
        print("Please run the script with an argument")
        print("./getBuildNumber.py 'major or minor'")
        sys.exit(2)

def main():

    #variable declaration
    version=''
    buildNO=''

    buildObj = operations.restAPI()
    objJson = buildObj.getRequest("content-packs")

    if 'Success' == objJson[0]:
        for eachObj in objJson[1]:
            if eachObj['name'] == 'myJenkinTest':
                version = eachObj['version']
    else:
        print("Failed to get the CP details",objJson)
        sys.exit(2)

    if version:
        if 'major' == sys.argv[1].lower():
            buildNo = float(int(float(version)) + 1)
            print(str(buildNo))
        if 'minor' == sys.argv[1].lower():
            buildNo = float(version) + 0.1
            buildNo = round(buildNo,1)
            print(str(buildNo))
    else:
        print("Failed to get VersionNo")
        sys.exit(2)

if __name__ == "__main__":
    usage()