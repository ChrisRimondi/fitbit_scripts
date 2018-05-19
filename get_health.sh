#!/bin/bash
source /home/ubuntu/fitbit_scripts/env_vars.sh


#Iterate over last week incase days were missed due to lack of sync
for i in {0..7}
do
	DATE=$(date -d "-$i day" +%Y-%m-%d)
	python /home/ubuntu/fitbit_scripts/sleep.py $DATE
	/usr/local/bin/aws s3 cp /home/ubuntu/fitbit_scripts/sleep_$DATE.csv s3://$S3_BUCKET/sleep/sleep_$DATE.csv
done

wait 10

for i in {0..7}
do
	DATE=$(date -d "-$i day" +%Y-%m-%d)
	python /home/ubuntu/fitbit_scripts/heart.py $DATE
/usr/local/bin/aws s3 cp /home/ubuntu/fitbit_scripts/heart_$DATE.csv s3://$S3_BUCKET/heartrate/heart_$DATE.csv
done
