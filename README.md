This repo is up as an example of how I would scrape housing data from a particular housing site.
The actual site url is not included - the names of the attribute ids have also been changed from the actual ids
there are parts of this script that could be functionised but I found the site can change on a regular basis with different sections 
e.g. price and address needing to be treated differently - I find the duplication easier to maintain than creating functions to try
cater for multiple cases

Project:
House Prices Analysis Project

Execution Order
(1) get_house_data.py
(2) house_analysis.py and houses_analysis.r (both independent of each other but dependent on output from step 1)

Notes:
get_house_data.py dependent on:
(1) target site
(2) google api url
(3) encrypted google api key (encrypt you key using https://github.com/rocklm/encrypting_text)
(4) google api cipher (cipher key generated using https://github.com/rocklm/encrypting_text)
(5) store files from note 4 and 5 in same directory as get_house_data.py
(6) get_address_coordinates.py is a module created to ease use and validate api paramaters
	needs to be in the same directory as get_house_data.py
(7)chromedriver.exe in the same directory as get_house_data.py

houses_analysis.py dependent on:
(1) encrypted mapbox api key (encrypt you key using https://github.com/rocklm/encrypting_text)
(2) mapbox api cipher (cipher key generated using https://github.com/rocklm/encrypting_text)

house_analysis.py and houses_analysis.r dependent on:
(1) house_data.xlsx from get_house_data.py - keep excel in same directory as house_analysis.py and houses_analysis.r





