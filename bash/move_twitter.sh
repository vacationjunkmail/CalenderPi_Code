#!/usr/bin/env bash

directory='/home/pi/Downloads/';
for f in $directory*twitter.txt
do
 #rsync -e ssh -hav --remove-source-files $f pi@192.168.1.105:/home/pi/Downloads 
  rsync -hav --remove-source-files $f pi@192.168.1.105:/home/pi/Downloads/
 echo "$f"
done

