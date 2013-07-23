#!/bin/bash
ARCH=i386

find "$PWD" -type d | while read directories
do

    for dir in  $directories
    do
	cd $dir
	echo $PWD
	for i in `ls -l | grep ^- | awk '{print $9}'`
	do
	    echo Stripped $i
	    ditto --rsrc --arch $ARCH $i bck_$i
	    mv bck_$i $i
	done
    done
done
