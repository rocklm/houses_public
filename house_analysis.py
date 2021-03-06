''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Script Name: 
House Analysis

Purpose:
Exploratory Analysis on Scraped House Prices

Script Dependencies:
mapbox api:
    mapbox_cipher.txt
    mapbox_api.txt

Parent Script(s):
encryption.py

Child Scripts(s):
get_house_data.py

Notes:
(1) build version indicates the module version the script was created on (pip modules only)
(2) UDF: user defined function (script notes will identify where a user created function is used)
(3) keep mapbox_api.txt/ mapbox_cipher.txt files in same directory as this program
(4) built on Python Version 3.9.1 64bit
(5) may need to adjust the 'directories' variable
(6) build version indicates the module version the script was created on (pip modules only)

Changes:

Name            Date            Version         Change
Lee Rock        27/12/2020      v1.0.0          initial version

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

import os
import sys
import subprocess
import pkg_resources

required = {'numpy', 'pandas', 'plotnine', 'gmplot'}
installed = {pkg.key for pkg in pkg_resources.working_set}
missing = required - installed

if missing:
    python = sys.executable
    subprocess.check_call([python, '-m', 'pip', 'install', *missing], stdout=subprocess.DEVNULL)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
set working directory to same loaction as script directory
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

os.chdir(os.path.dirname(os.path.abspath(__file__)))

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
temporarily include path of encryption module and current project
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

directories = ['c:\\', 'c:\\Side Projects\\encrypting_text']

for directory in directories:
    if directory not in sys.path:
        sys.path.insert(1,directory)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
required modules
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

from plotnine import geom_bar, ggplot, aes #install (build version: 0.7.1)
import pandas as pd #install (build version: 1.1.5)
import numpy as np #install (build version: 1.19.4)
import itertools
import gmplot #install (build version: 1.4.1)
import plotly.express as px #install (build version: 4.14.3)
from encryption import encrypt #found: https://github.com/rocklm/encrypting_text

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
Script User Defined Functions (UDF)
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#function to apply multiple stats to a vector at once
def desc_stats(x):

   # x = column/vector to be passed

    #dictionary holding methods
    method_dict = {
        'count': round(len(x), 2),
        'sum': round(np.nansum(x), 2),
        'avg': round(np.nanmean(x), 2),
        'min': round(np.nanmin(x), 2),
        'max': round(np.nanmax(x), 2),
        'Q1': round(np.nanquantile(x, 0.25), 2),
        'Median': round(np.nanmedian(x), 2),
        'Q3': round(np.nanquantile(x, 0.75), 2)
        }

    return method_dict

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#function to summarise data by groups and an aggregate function
#the desc_stats UDF can be used with this function to apply multiple 
#aggregations to a vector or field(s) at once
def grp_summarise(dataset, grp, agg_fields, func):

    #dataset = input dataset (pandas dataframe)
    #grp = a list [] of grouping variables e.g. [field_1] or [field_1, field_2]
    #agg_fields = a list [] of aggregation variables e.g. [field_1] or [field_1, field_2]
    #func = the aggregation function to be applied
   
    #list to store dataframe for each aggregated field by group(s)
    frame_list = []

   #pair each aggregation field with the function, store in dictionary
    func_dict = dict.fromkeys(agg_fields, func)
    #aggregate the chosen fields by group using the function stored in the dictionary
    agg_data = dataset.groupby(grp).agg(func_dict)
    #convert results to a dataframe keeping the row index as the group by fields

    #loop to convert each aggregation to a dataframe and add to dataframe list
    for field in agg_fields:
        frame = pd.DataFrame(agg_data[field].values.tolist(), index = agg_data.index)
        
        frame_list.append(frame)

    #conactonate dataframes of aggregated fields
    final_results = pd.concat(frame_list, axis = 1, keys = agg_fields)

    return final_results

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

#function to scale a vector between a range
def scale(vctr, new_min, new_max):

    old_min = min(vctr)
    old_max = max(vctr)
    old_range = old_max - old_min
    new_range = new_max - new_min
  
    scale_vals = []
    for val in vctr:
        scaled_val = int((((val - old_min) * new_range) / old_range) + new_min)
        scale_vals.append(scaled_val)

    return scale_vals

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import raw data from excel and drop the index column
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

raw = pd.read_excel('C:\\Side Projects\\houses\\house_data.xlsx', 
                    sheet_name='Sheet1', 
                    header = 0,
                    engine='openpyxl')

#drop index column
raw.drop(raw.columns[0], axis=1, inplace=True)


''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
descriptive stats on raw data
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#using  the desc_stats and grp_summarise UDFS created at the top of this script
prop_desc_stats = grp_summarise(raw, ['prop_type'], ['price', 'beds', 'baths'], desc_stats)
agent_desc_stats = grp_summarise(raw, ['agent'], ['price', 'beds', 'baths'], desc_stats)
prop_and_agent_desc_stats = grp_summarise(raw, ['prop_type', 'agent'], ['price', 'beds', 'baths'], desc_stats)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(prop_desc_stats)

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
maps
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''

#scale price to readable bubble size 
raw['price_scld'] = scale(raw['price'].fillna(0), 10, 300)

#open file read in encrypted API key
api_file = open('C:\\Side Projects\\houses\\mapbox_api.txt', 'r')
encrypted_api = api_file.readline()
api_file.close()

#open file read in encrypted API key
cipher_file = open('C:\\Side Projects\\houses\\mapbox_cipher.txt', 'r')
cipher = cipher_file.readline()
cipher_file.close()

#decrypted key
key = encrypt.decrypt_text(encrypted_api, cipher)

#create map
px.set_mapbox_access_token(key)
fig = px.scatter_mapbox(raw, lat="lat", lon="lng", color ="price", size="price_scld",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=30, zoom=10)
fig.show()

''' 
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
                    end of script
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
'''
