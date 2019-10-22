# osc2i2c


configuring Pi:

1. install i2c packages
sudo apt-get install python-smbus
sudo apt-get install i2c-tools


If you are using Raspian Linux 3.18 or later you need to go into the raspberry pi config utility and enable I2C.

```
sudo raspi-config
```
Select 5 Interfacing Options and then  P5 I2C. A prompt will appear asking Would you like the ARM I2C interface to be enabled?, select Yes, exit the utility and reboot your raspberry pi.

```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```
