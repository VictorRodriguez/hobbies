#!/bin/bash

while true; do
	DATE=`date`
	HOUR=`date +%H`
	while [ $HOUR -ne "00" ]; do
		echo "Whats jira status ?  / Como vas ? ""$DATE"
		sleep 36
		HOUR=`date +%H`
	done
done
