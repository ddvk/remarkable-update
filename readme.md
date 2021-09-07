# Simple Factory Reset (updater)
A hackish, quick and dirty update server implementation

## Usage
get an official update e.g.   
[rm2 2.7.0.51](https://eu-central-1.linodeobjects.com:443/remarkable-2/build/reMarkable%20Device%20Beta/RM110/2.7.0.51/2.7.0.51_reMarkable2.signed)  
[rm1 2.7.0.51](https://eu-central-1.linodeobjects.com:443/remarkable-2/build/reMarkable%20Device%20Beta/RM110/2.7.0.51/2.7.0.51_reMarkable.signed)  
drop it in:
`updates/`
on your host, start the server: `python serve.py`  
the server will use the machine's hostname, so that should be resolvable from the tablet

you may use the usb interface for the update, just find the ip address that was assigned to it and run the server e.g.  `python server.py 10.11.99.2'

on the device:

edit: `/usr/share/remarkable/update.conf`  
set the line: `SERVER=http://yourhost:8000`  
make sure you can ping/resolve `yourhost` from the device. 
if your dns sucks, add the entry to `/etc/hosts`, you may even use the usb interface ip address (10.11.99.2).

if you disabled the automatic updates, make sure the update-engine is running: `systemctl start update-engine`

trigger the update: `update_engine_client -check_for_update`  
or via the UI (check for update)

to observe the update progress: `journalctl -u update-engine -f`  


## To switch the partition i.e. boot the previous version
use the `switch.sh` script on the device

## Beta
It seems that the update server address (SERVER) is defined in the `/home/root/.config/xochitl.conf` file [Issue](https://github.com/ddvk/remarkable-update/issues/7)

