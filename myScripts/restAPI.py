#!/usr/bin/env python

import requests
import urllib3
import sys
import os
import time

sys.path.append(os.getcwd())
import operations

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #to Ignore SSL certificate

class restQuerry(object):

    def __init__(self):
        self.url = "https://130.175.106.166:8445/oo/rest/v2/"
        self.userName = "admin"
        self.password = "admin123"

    def postQuerry(self,setattr,payload):

        get_url = self.url + setattr
        with requests.session() as session:

            session.auth = (self.userName,self.password)
            get = session.get(get_url, verify=False)             # GET request #1 to get initial CSRF Token

            get = session.get(get_url, verify=False)             #GET request #2 to get second CSRF Token
            CSRF = get.headers['X-CSRF-TOKEN']
            headers = {'Content-Type': 'application/json', 'X-CSRF-TOKEN': CSRF}
            post = session.post(get_url, data=payload, headers=headers, verify=False)

            if post.ok and post.status_code == 201:
                try:
                    return "Success", post.json()
                except Exception as e:
                    return ("post requested failed", e,post.text.encode('utf8'))
            else:
                return "Failed",post.text.encode('utf8')


def main(uuid,runName=None):

    #default runName is run1
    if runName == None:
        runName = "run1"

    restObj = restQuerry()
    data = "{\"flowUuid\": \"" + uuid + "\"," + "\"runName\": \"" + runName + "\"}"
    postResult = restObj.postQuerry("executions",data)

    if 'Success' == postResult[0]:
        executionId = postResult[1]
    else:
        print("Flow Execution Failed",postResult)
        sys.exit(2)

    # Get the execution Status
    count = 20
    buildObj = operations.restAPI()
    Executionurl = "executions/" + str(executionId) + "/summary"

    while (count>0):
        count-=1
        time.sleep(10)
        objJson = buildObj.getRequest(Executionurl)

        if 'Success' == objJson[0]:
            jsonouput = objJson[1]
        else:
            print("Failed to check the flow status", objJson)
            sys.exit(2)

        if jsonouput[0]['status'] == 'COMPLETED' and jsonouput[0]['resultStatusName'] == 'success':
            print("Flow Execution Success")
            sys.exit(0)
        elif jsonouput[0]['status'] == 'COMPLETED' and jsonouput[0]['resultStatusName'] == 'ERROR':
            print("Flow failed with Errors")
            sys.exit(1)
        elif jsonouput[0]['status'] == 'RUNNING':
            print("Flow Status : Running")
        elif jsonouput[0]['status'] == 'PAUSED':
            print("Flow Paused, waiting for the userInput!")
        elif jsonouput[0]['status'] == 'CANCELED':
            print("Flow canceled by administrator or user!")
            sys.exit(2)
        else:
            print("Flow failed to complete with in {} Seconds",300)



if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1],sys.argv[2])
    elif len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Please run with an argument, Default runName is run1")
        print("./restAPI UUID runName")

