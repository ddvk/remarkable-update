# Simple Factory Reset (updater)

## Usage
get an official update e.g. [2.5.0.27](https://eu-central-1.linodeobjects.com:443/remarkable-2/build/reMarkable%20Device%20Beta/RM110/2.5.0.27/2.5.0.27_reMarkable2.signed), drop it in:
`updates/`
start the server: `python serve.py`  

on the device:

edit: `/usr/share/remarkable/update.conf`  
 set the line: `SERVER=http://yourhost:8000`  
 trigger the udpate: `update_engine_client -check_for_update`  
 or via the UI (check for update)

to observe the update: `journalctl -u update-engine -f`  


## To switch the partition
use the `switch.sh` script on the device

