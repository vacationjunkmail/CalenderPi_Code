#!/usr/bin/env bash

home_path=$HOME

alias_file="$home_path/.bashrc_aliases";
directory="$home_path/Downloads/";

rsync_addr=''
reg_ex="'ssh (.*)'"

while IFS= read -r line
do
  if [[ "$line" == *"FirstPi"* ]]; then
    rsync_addr="$line"
  fi
done < $alias_file

c=${#rsync_addr}
z=0

if [ -z "$rsync_addr" ]; then
	echo "$rsync_addr ______"
fi


[[ $rsync_addr =~ $reg_ex ]]

rsync_addr=${BASH_REMATCH[1]};
if [ -n "$rsync_addr" ]; then
	for f in $directory*twitter.txt
		do
			echo $f
	 		##rsync -e ssh -hav --remove-source-files $f pi@192.168.1.105:/home/pi/Downloads 
			rsync -hav --remove-source-files $f pi@$rsync_addr:/home/pi/Downloads/
			#echo "$f"
	done
else
	echo "No alias found with with the name of FirstPi"
fi
