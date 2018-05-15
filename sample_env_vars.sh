#!/bin/bash

#export display so I can run this via cron
export DISPLAY=:10.0
#USER_ID and Secret come from Fitbit dev portal
export FITBIT_USER_ID=example_user_id
export FITBIT_CLIENT_SECRET=example_secret
#To get around oauth automation limitations need to set browser for xfce
export BROWSER=firefox
#s3 bucket where I uploaded my csv files
export S3_BUCKET=mybucket
