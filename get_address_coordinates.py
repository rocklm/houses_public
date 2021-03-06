''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Script Name: 
Geocoding Addresses

Purpose:
Return the longtitude and latitude for an address

Script Dependencies:
A GOOGLE Maps API key

Parent Script(s):
N/A

Child Scripts(s):
get_house_data.py

Notes:
(1) built on Python Version 3.9.1 64bit
(2) build version indicates the module version the script was created on (pip modules only)

Name            Date            Version         Change
Lee Rock        21/12/2020      v1.0.0          initial version

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    start of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
install required non standard external modules if missing
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import sys
import subprocess
import pkg_resources

required = {'requests'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
required modules
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import requests #install (build version: 2.25.1)
import json
import urllib
import os

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
set working directory to same loaction as script directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))


''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
API Key Validation Class
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

class api_key:
    
    #initialisation function
    def __init__(self, key):
        self.key = key
    
    #return validated api key when called
    @property
    def key(self):
        return self.__key

    #logic to ensure the api key is not blank and is a text/string data type
    #if the key is not text or is blank error messages will be returned
    @key.setter
    def key(self, key):
        if key == '':
            raise ValueError("API key cannot be blank")
        else:
            if isinstance(key, str):
                self.__key = key
            else:
                raise TypeError("API key must be string (text) type") 
            
        
''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
API Website Validation Class
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

class api_site:
    
    #initialisation function
    def __init__(self, site):
        self.site = site
    
    #return validated api site when called
    @property
    def site(self):
        return self.__site

    #logic to ensure the api site is not blank and is a text/string data type
    #if the site is not text or is blank error messages will be returned
    @site.setter
    def site(self, site):
        if site == '':
            raise ValueError("API site cannot be blank")
        else:
            if isinstance(site, str):
                self.__site = site
            else:
                raise TypeError("API site must be string (text) type") 

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
geocode Class
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

class geocode(api_key, api_site):
     
    #initialisation function
    def __init__(self, key, site, address):
        self.key = key
        self.site = site
        self.address = address
    
    #function to convert address into coordinates
    def geocode_info(self):

        #parameters for api url - the target address and the api key
        params = {"address": self.address, 
                  "key": self.key}

        #call the api
        req = requests.get(f"{self.site}{urllib.parse.urlencode(params)}")
        #return information
        return json.loads(req.content)


''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    end of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
