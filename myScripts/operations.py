#!/usr/bin/env python

import requests
import urllib3
import sys
import os
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) #to Ignore SSL certificate

class restAPI(object):

    def __init__(self):
        self.url = "https://130.175.106.166:8445/oo/rest/"
        self.userName = "admin"
        self.password = "admin123"

    def getRequest(self,getattr):

        getUrl = self.url + getattr
        getObj =  requests.get(getUrl,auth=(self.userName,self.password),verify=False)

        if getObj.ok and getObj.status_code == 200 :
            try:
                return "Success",getObj.json()
            except Exception as e:
                return ("get requested failed",e)
        else:
            return "Failed"


    def putRequest(self,putattr,path):

        putUrl = self.url + putattr
        fileObj = open(path,'rb')
        putObj = requests.put(putUrl,data = fileObj, auth=(self.userName,self.password),verify=False)

        if putObj.ok and putObj.status_code == 201:
            try:
                fileObj.close()
                return "Success",putObj.json()
            except Exception as e:
                fileObj.close()
                return ("post requested failed", e)
        else:
            fileObj.close()
            return "Failed"
