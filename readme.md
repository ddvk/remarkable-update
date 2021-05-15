# Simple Factory Reset (updater)

## Usage
get an official update e.g.   
[rm2 2.7.0.51](https://eu-central-1.linodeobjects.com:443/remarkable-2/build/reMarkable%20Device%20Beta/RM110/2.7.0.51/2.7.0.51_reMarkable2.signed)  
[rm1 2.7.0.51](https://eu-central-1.linodeobjects.com:443/remarkable-2/build/reMarkable%20Device%20Beta/RM110/2.7.0.51/2.7.0.51_reMarkable.signed)  
drop it in:
`updates/`
start the server: `python serve.py`  

on the device:

edit: `/usr/share/remarkable/update.conf`  
set the line: `SERVER=http://yourhost:8000`  

if you disabled the automatic updates, make sure the update-engine is running: `systemctl start update-engine`

trigger the update: `update_engine_client -check_for_update`  
or via the UI (check for update)

to observe the update progress: `journalctl -u update-engine -f`  


## To switch the partition
use the `switch.sh` script on the device

