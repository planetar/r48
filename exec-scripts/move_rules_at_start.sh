#!/bin/bash
#######################
#
# clean up the start process 
#  starting rules in a sorted manner after openhab2 got it's feet on the ground
#  called from systemd pre and post start 
#  to rename *.rules away initially and then rename them back one by one
#  
#  /etc/systemd/system/openhab2.service.d/.#override.conf041cd66becaa4539
#
# $3 allows to distinguish between pre and post action 
#
# REF: https://community.openhab.org/t/cleaning-up-the-startup-process-renaming-rules-windows-possible/38438/9


ORG=$1
NEW=$2
THX=$3
DUR=1
IGNORE=005_start.rules

for f in /etc/openhab2/rules/*.${ORG};
do
    CURRENT=$(basename $f)
    if [ "$CURRENT" == "$IGNORE" ]    
    then
    	echo "ignoring $IGNORE"
    else
        OLDFILE=$f
        NEWFILE=${f%$ORG}$NEW
        mv "$OLDFILE" "$NEWFILE"
    fi
    # let some time between each load
    if [ "$THX" == "POST" ]
    then
	/bin/sleep $DUR
    fi
done

# some things left on startup
if [ "$THX" == "POST" ]
then
#     /usr/bin/touch /etc/openhab2/things/tradfri.things
      /usr/bin/touch /etc/openhab2/misc/exec.whitelist
      echo "touched /etc/openhab2/misc/exec.whitelist"

fi


