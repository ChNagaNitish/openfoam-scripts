#!/bin/bash
begin=$1
dest=$2
procs=$3
perProc=$4
i=$5
dirList=($(find . -maxdepth 1 -type d -name "[0-9]*\.[0-9]*" -printf "%f\n" | sort -n))
if [ $i -ne $procs ]; then
	h=("${dirList[@]:begin:perProc}")
else
	h=("${dirList[@]:begin}")
fi
for folder in "${h[@]}";
do
#	echo $begin $dest $folder
	cp -r "$folder" "$dest/"
done
