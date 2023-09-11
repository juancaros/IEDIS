#Import libraries, pytrends, pandas and time to add waiting time between queries 

import time
import pandas as pd   
from pytrends.request import TrendReq


# Only need to run this once, the rest of requests will use the same session.
pytrends = TrendReq(hl='es', tz=360)

# keywords
keywords = ['ansiedad', 'estrés', 'tristeza', 'depresión']
keywords.sort() # Sort the list

# locations
geo = ['ES-AN', 'ES-AR', 'ES-CN', 'ES-CB', 'ES-CL', 'ES-CM', 'ES-CT', 'ES-CE', 'ES-MD', 'ES-VC', 'ES-EX', 'ES-GA', 'ES-IB', 'ES-RI', 'ES-ML', 'ES-NC', 'ES-PV', 'ES-AS', 'ES-MC' ]
geo.sort()

#timeframe 
timeframe='2018-06-01 2019-06-30'

# Perform searches
wait = 6 # in seconds
print('Number of queries to do: ', len(keywords) * len(geo))

# Prepare containers
trends = dict.fromkeys(geo)
errors_list = []
cnt = 1

# Start loops
for g in geo:
    trends[g] = {}
    for k in keywords:
        try:
            time.sleep(wait)
            pytrends.build_payload([k], timeframe=timeframe, geo=g, gprop='')
            trends[g][k] = pytrends.interest_over_time()[k]
            #print(cnt, 'Success: ', g, k)

        except:
            print(cnt, ') Error: ', g, ' & ', k)
            errors_list.append([g,k])
        cnt+=1
        
print('\nDone -', len(errors_list), 'errors left')

dict_of_trends = {g: pd.DataFrame(k) for g,k in trends.items()}
data_df = pd.concat(dict_of_trends, axis=1)
data_df.to_csv('trends.csv',index=False)
data_df.head() # Check data