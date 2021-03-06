#!/usr/bin/env python

import sys
import os
import json
import re

sys.path.append(os.getcwd())
import operations

def usage():
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Please run the script with an argument")
        print("./uploadFile.py 'buildNumber'")
        sys.exit(1)

def main(buildNo):

    #find the latest jar file

    dirList = os.listdir(os.getcwd())
    pattern = ".*" + str(buildNo) + ".*"
    for eachlist in dirList:
        if re.findall(pattern,str(eachlist)):
            arg = eachlist

    if not(arg):
        print("failed the get latest jar")
        sys.exit(1)
    # variable declaration
    flag = 0
    shortNameCp = arg.split(".jar")[0]
    pathCp = os.getcwd() + "/" + arg
    putURL = "content-packs" + "/" + shortNameCp

    uploadObj = operations.restAPI()
    uploadJson = uploadObj.putRequest(putURL,pathCp)

    if 'Success' == uploadJson[0]:
        uploadJsonStr = str(uploadJson[1])
        if 'Success' in uploadJsonStr:
            print("Upload request is success. Verifying it!!")
        else:
            print("Failed to upload the jar File")
            sys.exit(2)
    else:
        print("Upload jar file ",uploadJson)
        sys.exit(2)

    objJson = uploadObj.getRequest("content-packs")
    if 'Success' == objJson[0]:
        for eachObj in objJson[1]:
            if eachObj['name'] == 'myJenkinTest' and eachObj['version'] == str(buildNo):
                flag = 1
                print("Succesfully uploaded the jar file",arg)
        if flag == 0:
            print("Failed to verify the CP details after upload")
            sys.exit(1)
    else:
        print("Failed to get the CP details after upload",objJson)
        sys.exit(2)

if __name__ == "__main__":
    usage()
