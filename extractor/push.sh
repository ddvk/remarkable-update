#!/bin/sh
set -e
IMAGE=$1
DEVICE=root@10.11.99.1

CURRENT=$(ssh $DEVICE "mount -v | grep  'on / ' | cut -f1 -d ' '")
OLD_PART="${CURRENT: -1}"

if [[ $OLD_PART -eq '2' ]]; then 
    NEW_PART=3
else
    NEW_PART=2
fi
NEW_DEVICE="/dev/mmcblk1p${NEW_PART}" #should be 2 or 3 at the end
echo "install to: $NEW_DEVICE"
echo "fallback: $OLD_PART"

ssh $DEVICE  << EOF
echo $OLD_PART
EOF

echo "Here be dragons"
dd if=$IMAGE | ssh $DEVICE "dd of=$NEW_DEVICE" 

ssh $DEVICE  << EOF
fw_setenv upgrade_available 1
fw_setenv bootcount 0
fw_setenv fallback_partition $OLD_PART
fw_setenv active_partition $NEW_PART
EOF
echo "Reboot the device"

