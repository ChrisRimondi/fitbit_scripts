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

yesterday = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime ("%Y%m%d"))
yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime ("%Y-%m-%d"))
today = str(datetime.datetime.now().strftime ("%Y%m%d"))
today2 = str(datetime.datetime.now().strftime ("%Y-%m-%d"))

#get sleep data / should be yesterday
fitbit_stats3 = auth2_client.sleep(date=yesterday2)
stime_list = []
sval_list = []



for i in fitbit_stats3['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])
sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
sleepdf['date'] = yesterday
sleepdf['year'] = datetime.datetime.strptime(yesterday2,"%Y-%m-%d").year 
sleepdf['month'] = datetime.datetime.strptime(yesterday2,"%Y-%m-%d").month
sleepdf['day'] = datetime.datetime.strptime(yesterday2,"%Y-%m-%d").day
sleepdf['dow'] = datetime.datetime.strptime(yesterday2,"%Y-%m-%d").isoweekday() 
sleepdf.to_csv('sleep_' + \
               yesterday2+'.csv', \
               columns = ['date','Time','State','Interpreted','year','month','day','dow'],header=True, \
               index = False)



#get sleep data / should be today
fitbit_stats3 = auth2_client.sleep(date='today')
stime_list = []
sval_list = []



for i in fitbit_stats3['sleep'][0]['minuteData']:
    stime_list.append(i['dateTime'])
    sval_list.append(i['value'])
sleepdf = pd.DataFrame({'State':sval_list,
                     'Time':stime_list})
sleepdf['Interpreted'] = sleepdf['State'].map({'2':'Awake','3':'Very Awake','1':'Asleep'})
sleepdf['year'] = datetime.datetime.strptime(today2,"%Y-%m-%d").year
sleepdf['date'] = today
sleepdf['month'] = datetime.datetime.strptime(today2,"%Y-%m-%d").month
sleepdf['day'] = datetime.datetime.strptime(today2,"%Y-%m-%d").day
sleepdf['dow'] = datetime.datetime.strptime(today2,"%Y-%m-%d").isoweekday()
sleepdf.to_csv('sleep_' + \
               today2+'.csv', \
               columns = ['date','Time','State','Interpreted','year','month','day','dow'],header=True, \
               index = False)
