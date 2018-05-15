#!/bin/bash
source env_vars.sh

python sleep.py
DATE=$(date +%Y-%m-%d)
YESTERDAY=$(date -d "-1 day" +%Y-%m-%d)
/usr/local/bin/aws s3 cp sleep_$DATE.csv s3://$S3_BUCKET/sleep/sleep_$DATE.csv
/usr/local/bin/aws s3 cp sleep_$YESTERDAY.csv s3://$S3_BUCKET/sleep/sleep_$YESTERDAY.csv

wait 10
python heart.py
/usr/local/bin/aws s3 cp heart_$YESTERDAY.csv s3://$S3_BUCKET/heartrate/heart_$YESTERDAY.csv
