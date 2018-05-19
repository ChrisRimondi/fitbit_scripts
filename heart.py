import fitbit
import gather_keys_oauth2 as Oauth2
import numpy as np
import pandas as pd
import datetime
import sys
import os

try:  
   USER_ID = os.environ["FITBIT_USER_ID"]
except KeyError: 
   print "Please set the environment variable FITBIT_USER_ID"
   sys.exit(1)

try:
   CLIENT_SECRET = os.environ["FITBIT_CLIENT_SECRET"]
except KeyError:
   print "Please set the environment variable FITBIT_CLIENT_SECRET"
   sys.exit(1)


"""for obtaining Access-token and Refresh-token"""

server = Oauth2.OAuth2Server(USER_ID, CLIENT_SECRET)
server.browser_authorize()

ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])


"""Authorization"""
auth2_client = fitbit.Fitbit(USER_ID, CLIENT_SECRET, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

date_query = sys.argv[1]

#get heart rate data / should be yesterday
fitbit_stats2 = auth2_client.intraday_time_series('activities/heart', base_date=date_query, detail_level='1sec')
stats2 = fitbit_stats2
time_list = []
val_list = []
for i in stats2['activities-heart-intraday']['dataset']:
    val_list.append(i['value'])
    time_list.append(i['time'])

heartdf = pd.DataFrame({'Heart Rate':val_list,'Time':time_list})
heartdf['date'] = date_query
heartdf['year'] = datetime.datetime.strptime(date_query,"%Y-%m-%d").year 
heartdf['month'] = datetime.datetime.strptime(date_query,"%Y-%m-%d").month
heartdf['day'] = datetime.datetime.strptime(date_query,"%Y-%m-%d").day
heartdf['dow'] = datetime.datetime.strptime(date_query,"%Y-%m-%d").isoweekday() 
heartdf.to_csv('heart_'+ \
               date_query+'.csv', \
               columns=['date','Time','Heart Rate','year','month','day','dow'], header=True, \
               index = False)

