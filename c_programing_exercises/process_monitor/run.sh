#!/bin/bash
counter=0
date > myprog.log
while [ $counter -le 10 ]
do
echo Errors: $counter Loops: $counter 2>&1 | tee -a myprog.log
((counter++))
sleep 10
done


