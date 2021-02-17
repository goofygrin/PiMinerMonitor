# PiMinerMonitor
Monitor your mining rig using a Raspberry Pi!

This is based on [this excellent guide from Adafruit](https://learn.adafruit.com/pi-hole-ad-blocker-with-pi-zero-w) for setting up a Raspberry Pi as a pihole ad blocking service.

Currently the code supports Ethermine, but Flexpool should be pretty easy to setup.

Once it's running it will show the current unpaid balance, the USD value of that balance, and the USD-ETH value.  If the number of workers is <2 or the number of invalid shares is >= 3 then the unpaid balance will be red.

By pressing the top button of the display for a second, it will toggle to a more detailed view with the hash rate, number of workers, the stale and invalid share counts. Holding the button again will toggle back to the simpler display.

Both displays will show a 5 minute countdown to the next refresh.

## Parts
1. [Raspberry Pi](https://www.microcenter.com/product/502843/raspberry-pi-zero-wh---with-pre-soldered-headers) - I used a Raspberry Pi Zero WH (H means it has the headers pre-soldered on) - $11.99 @ Microcenter
2. [Adafruit Mini PiTFT](https://www.adafruit.com/product/4393) - $14.99 @ Microcenter
3. MicroSD card
4. Power Supply for the pi

## Setup

Install the PiTFT onto the pi.

Follow the instructions [here](https://www.raspberrypi.org/software/) to install Raspberry Pi OS Lite on the SD card.

Once the bare OS is copied to the card, plug it back into your computer and prep it for headless running (you can follow the [official instructions](https://www.raspberrypi.org/documentation/configuration/wireless/headless.md) if you'd like):
- add a blank file named ssh to the card to turn on ssh by default
- add a file named wpa_supplicant.conf with the following content (updating to replace the three settings with your info):
  ```
  ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
  update_config=1
  country=<Insert 2 letter ISO 3166-1 country code here>

  network={
    ssid="<Name of your wireless LAN>"
    psk="<Password for your wireless LAN>"
  }
  ```

Insert the SD card into the pi and power it on.  With a pi zero the little green led will flicker as it boots.

Look in your wireless router's DHCP list to find the IP address of the pi.

Launch your favorite SSH program (PuTTY on windows or ssh in a shell on OSX/linux) and ssh into the pi.  The default login is pi/raspberry.

Run the following commands:
1. Update your Pi
   ```
   sudo apt-get update
   sudo apt-get upgrade
   ```
2. Install pip
   ```
   sudo apt-get install python3-pip   
   ```
3. Install setup tools
   ```
   sudo pip3 install --upgrade setuptools
   ```
4. Install the Adafruit tools
   ```
   sudo pip3 install --upgrade adafruit-python-shell
   ```
5. Get the setup script and run it (this sets up a number of things and turns on SPI to talk to the display)
   ```
   wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
   sudo python3 raspi-blinka.py
   ```
6. Say yes to setting Python3 as the default
7. When prompted to reboot, select yes
8. Once the pi is rebooted, ssh back into it
9. Download the script
   ```
   wget https://raw.githubusercontent.com/goofygrin/PiMinerMonitor/main/miner.py
   ```
10. Run the script, passing in the options
   ```
   sudo python3 miner.py <ethermine|flexpool> <wallet>
   ```
11. The script should run and you should see the display light up and then start displaying the base data and a countdown.
12. If everything is working, press ctrl-c to stop the process.
13. Edit the rc.local to get the script to run on bootup.
   ```
   sudo nano /etc/rc.local
   ```
14. Add the following line above the "exit 0" line
   ```
   sudo python3 ~pi/miner.py > ~pi/miner.log &
   ```
15. Press ctrl-x, select yes to save, and exit the file
16. Reboot the pi to make sure this worked correctly
   ```
   sudo shutdown -r now
   ```
