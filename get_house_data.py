''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Script Name: 
House Price Scraper

Purpose:
Return information regatding listed properties on daft.ie

Script Dependencies:
google API key:
    goog_cipher.txt
    goog_api.txt
google maps api url

Parent Script(s):
get_addresss_coordinates.py
encryption.py

Child Scripts(s):
N/A

Notes:
(1) google api url may change through time
(2) keep goog_api.txt/ goog_cipher.txt files in same directory as this program
(3) built on Python Version 3.9.1 64bit
(4) may need to adjust the 'directories' variable
(5) build version indicates the module version the script was created on (pip modules only)

Changes:

Name            Date            Version         Change
Lee Rock        03/12/2020      v1.0.0          initial version

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    start of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 standard required modules
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

import re
import sys
import os
import bs4 as bs #install (build version: 2.25.1)
import pandas as pd #install (build version: 1.1.5)
import concurrent.futures
from urllib.request import Request, urlopen
from selenium import webdriver #install (build version: 3.141.0)
from datetime import datetime

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
set working directory to same loaction as script directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

os.chdir(os.path.dirname(os.path.abspath(__file__)))

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
temporarilily include path of encryption module and current project
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

directories = ['c:\\Side Projects\\encrypting_text', 
               'c:\\Side Projects\\houses']

for directory in directories:
    if directory not in sys.path:
        sys.path.insert(1,directory)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
 user created required modules
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
from get_address_coordinates import geocode #user created (same directory as this script)
from encryption import encrypt #found: https://github.com/rocklm/encrypting_text


''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
start time of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
print('Starting script...')
start_time = datetime.now().replace(microsecond = 0)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
target site - using selenium to dymanically identify total number
of records - unable to scrape this using urllib container not visible
for some reason
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#daft.ie base url site to get the total number of search results and results per page
base_site = 'https://target_housing_site'

#chrome driver location may need to be changed here
driver = webdriver.Chrome(executable_path= r'c:\\Side Projects\\houses\\chromedriver.exe')

#get html of base site
driver.get(base_site)
soup = bs.BeautifulSoup(driver.page_source, features='html.parser')


''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Extract number of records and search results per page
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#get the sentence stating the number of results per page and total number of records e.g. showing 1 - 20 of 480
results_pp_and_ttl_recs = soup.find('p', attrs={'att_id':'pagination-results'}).text.replace(',','')
#get the number after "of" (total result count)
ttl_results = int(re.search('of(.*)', results_pp_and_ttl_recs).group(1))
#get the number between "-" and "of" (max number of results shown per page)
results_per_page = int(re.search('-(.*) of', results_pp_and_ttl_recs).group(1))

#exit chrome session 
driver.close()

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
while loop to grab data

target site has a "from=0" at the end of the url
the zero indicates the starting point to return a set number of records on the page
there is a maximum number of records that can be displayed on the page e.g. 20
so if "from=0" is changed to "from=20" we move onto page 2 and collect the next 20 records 
if "from=20" is changed to "from=40" we move onto page 3 to collect the next 20 records etc

- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

###loop initialisaions###

#store the starting index to grab records
#this is increased by the max number of records allowed to be displayed each iteration
#this allows us to move onto the next page
starting_index = 0 

#create empty data frame to store housing information - data cleaning wil be needed
#eircode latititude and longititude will be gotten by funnelling the address 
#into google maps api
scraped_house_info = pd.DataFrame(columns=['price', 'prop_type','floor_area', 'agent', 'beds',
                                   'baths', 'address'])


while starting_index < ttl_results:

    ''' 
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    connect to the ith webpage
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    '''

    #remove the initial starting index from the base site
    url_rm = base_site.replace(base_site[-1], '')
    #attach the new starting index to call X set of records
    url = url_rm + str(starting_index)
    #increase the starting index by the max records displayed per page
    #for next iteration
    starting_index += results_per_page
   
    ''' 
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    Get html for ith webpage
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    '''

    #using urllib to scrape housing data as it's faster than selenuim
    #send request to get the site using mozilla
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #open the site
    page = urlopen(req).read()
    #scrape and store the html
    soup = bs.BeautifulSoup(page, features='html.parser')
    #extract the search result container
    search_results = soup.find_all('li', attrs={'att_id': re.compile('^result-')})

    ''' 
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    loop to extract housing data from each information container 
            ie extract information for each house
    - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    '''

    for info_cont in search_results:
        
        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the price
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
     
        try:
            #find the price sub container for the poperty
            price_div =  info_cont.find('div', attrs={'att_id':'price'})
            #extract the house price - '\D' removes everything but numbers ie the price
            price = float(re.sub('\D', '', price_div.find('p').text))
        except:
            price = None

        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the property type
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
        
        try:
            #extract the property type for the property
            prop_type = info_cont.find('p', attrs={'att_id':'prop_type'}).text
        except:
            prop_type = None

        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the address
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
        
        try:
            #extract the address for the property
            address = info_cont.find('p', attrs={'att_id':'address'}).text
        except:
            address = None

        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the number of beds
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
        
        try:
            #extract the number of bedrooms for the property
            bed = float(re.sub('\D', '', info_cont.find('p', attrs={'att_id':'bed_no'}).text))
        except:
            bed = None
       
        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the number of baths
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
        
        try:
            #extract the number of bathrooms for the property
            bath = float(re.sub('\D', '',info_cont.find('p', attrs={'att_id':'bath_no'}).text))
        except:
            bath = None
       
        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the ber rating
        need to set up QT
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
        
        #try:
            #extract the ber image hyper link for the property
            #ber  = info_cont.find('img', attrs={'att_id':'ber-image'})['src']
            #extract the ber rating from the image link
            #ber = ber_img_src.split('images/',1)[1]
        #except:
            #ber = None

        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the agent
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
        
        try:
            #extract the agent name for the property
            agent = info_cont.find('span', attrs={'att_id':'agent'}).text
        except:
            agent = None

        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        Get the floor area
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''
        
        try:
            #extract the agent name for the property
            floor_area = info_cont.find('p', attrs={'att_id':'floor'}).text
        except:
            floor_area = None

        ''' 
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        append data for property to data frame
        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
        '''

        #append information regarding a particular peoperty as a row in the dataframe
        scraped_house_info.loc[len(scraped_house_info)] = [price, prop_type, floor_area, agent, bath, bed, address]

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
use google API to get eircode longtitude and latitude of address
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#open file read in encrypted API key
api_file = open('goog_api.txt', 'r')
encrypted_api = api_file.readline()
api_file.close()

#open file read in encrypted API key
cipher_file = open('goog_cipher.txt', 'r')
cipher = cipher_file.readline()
cipher_file.close()

#decrypted key
key = encrypt.decrypt_text(encrypted_api, cipher)
#google api url 
site = 'https://maps.googleapis.com/maps/api/geocode/json?'

#empty dataframe to store eircode and coordinates
api_data = pd.DataFrame(columns=['lat', 'lng', 'eircode'])

#for loop to return the coordinates and eircode for each address
for address in scraped_house_info['address']:
   
    #retun json object holding address information
    info = geocode(key, site, address).geocode_info()

    #if no results are returned
    if info['status'] == 'ZERO_RESULTS':

        coords_lat = None
        coords_lng = None

    else:
         #extract the coordinates for the address
        coords = info.get("results")[0].get("geometry").get("location")
        coords_lat = coords['lat']
        coords_lng = coords['lng']

    #extract the eircode for the adddress - return none if no eircode is available
    try:
        eircode = info.get("results")[0].get("address_components")[6].get('long_name') 
    except:
        eircode = None

    #append api information to dataframe
    api_data.loc[len(api_data)] = [coords_lat, coords_lng, eircode]

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
concatonate the scraped data with api data
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

house_data = pd.concat([scraped_house_info, api_data], axis=1).reindex(scraped_house_info.index)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
export data to excel
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

house_data.to_excel("house_data.xlsx") 

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
end time of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

print('Finished Script: ' + str(datetime.now().replace(microsecond = 0) - start_time))

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    end of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

