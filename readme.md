# Simple Factory Reset (updater)

A hackish, quick and dirty update server implementation

## Usage

1. Clone this Repo

1. Obtain an official release that you would like to upgrade (er, downgrade) to. A [list of firmware releases can be found here](https://thelastzombie.github.io/remarkable-firmware/).

1. Put your firmware release in `./updates`.

1. Figure out the hostname of the computer you are connecting your remarkable to. If you are connecting to USB it will likely be `10.11.99.2`. If your ReMarkable device is connected to your local wifi, it may also work to use a local IP address such as `192.168.1.25`. The docs will use `10.11.99.2` as the hostname. If you have a different hostname, adjust accordingly.

1. Start the mock upgrade server. (This assumes you are running python3)

   ```shell
   python serve.py 10.11.99.2
   ```

1. SSH into your ReMarkable device and edit `/usr/share/remarkeable/update.conf`:

   ```shell
   ssh root@10.11.99.1
   vim /usr/share/remarkeable/update.conf
   ```

1. Add the following line to the `update.conf` file:

   ```text
   SERVER=http://10.11.99.2:8000
   ```

1. Run an automatic update.

### Via ReMarkable UI

1. Go to Menu -> Settings -> General: click on the Software Version.

1. Tap Check for Updates. It should download and install the update.

1. Once it is complete, it should prompt you to tap to reboot your device.

### Via the CLI

1. In the ReMarkable Terminal, make sure `update-engine` is running:

   ```shell
   systemctl start update-engine
   ```

1. Trigger the update:

   ```shell
   update_engine_client -check_for_update
   ```

1. Observe the update progess.

   ```shell
   journalctl -u update-engine -f
   ```

1. Once it is complete, reboot the device.

   ```shell
   reboot
   ```

## To switch the partition i.e. boot the previous version

1. Copy the `switch.sh` script to the device.

   ```shell
   scp switch.sh root@10.11.99.1:~
   ```

1. SSH into reMarkable and run the script.

   ```shell
   ssh root@10.11.99.1
   ./switch.sh
   ```

1. Reboot the device for changes to take effect.

   ```shell
   reboot
   ```

## Beta

It seems that the update server address (SERVER) is defined in the `/home/root/.config/xochitl.conf` file [Issue](https://github.com/ddvk/remarkable-update/issues/7)
