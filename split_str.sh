#!/bin/zsh

fileName=$1
content=`cat $fileName`

for i in $(echo $content | tr " " "\n")
do
	# if [ ${#i} -eq 64 ]; then
		echo $i
	# fi
done