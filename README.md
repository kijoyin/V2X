# VZX

## Warning

PIN 33 will crash bluetooth (a day wasted)

## Setting up Pi for Bluetooth Serial Conneciton

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install bluetooth

sudo apt-get install bluez

sudo apt-get install python-bluez

sudo pip3 install pybluez (some file or folder missing error at this point)

Edit /etc/systemd/system/dbus-org.bluez.service and add '-C' after 'bluetoothd'. Reboot.

sudo sdptool add SP (Permission denied error once i run the python code at this point)

Running as SUDO fixed the issue for me

Also i this point I have the bluetooth discoveralbe and connected to my Anroid phone (Not sure this is needed)

## Sending message from Phone

Find the MAC address of pi bluetooth - Run hciconfig on PI to get that

## Setting up Python to run as a server
sudo nano /lib/systemd/system/carserver.service

### Add the following text

[Unit]
 Description=Carserver
 After=multi-user.target

 [Service]
 Type=idle
 ExecStart=/usr/bin/python /home/pi/Desktop/carserver.py

 [Install]
 WantedBy=multi-user.target
 
 ### Save the text and Run the following commands
 sudo chmod 644 /lib/systemd/system/carserver.service
 sudo systemctl daemon-reload
 sudo systemctl enable carserver.service
 sudo reboot

