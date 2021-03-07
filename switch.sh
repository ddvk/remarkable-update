#!/bin/bash
# switches the active root partition

fw_setenv "upgrade_available" "1"
fw_setenv "bootcount" "0"

OLDPART=$(fw_printenv -n active_partition)
if [ $OLDPART  ==  "2" ]; then
    NEWPART="3"
else
    NEWPART="2"
fi
echo "new: ${NEWPART}"
echo "fallback: ${OLDPART}"

fw_setenv "fallback_partition" "${OLDPART}"
fw_setenv "active_partition" "${NEWPART}"
