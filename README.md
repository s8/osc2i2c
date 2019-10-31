# osc2i2c


configuring Pi:

1. Install i2c packages
```
sudo apt-get install python-smbus
sudo apt-get install i2c-tools
```


2. Enable I2C.

```
sudo raspi-config
```
Select 5 Interfacing Options and then  P5 I2C. A prompt will appear asking Would you like the ARM I2C interface to be enabled?, select Yes, exit the utility and reboot your raspberry pi.

```
sudo apt-get update
sudo apt-get upgrade
sudo reboot
```

3. Install Adafruit PCA9685 libraries
```
sudo apt-get install git build-essential python-dev
cd ~
git clone https://github.com/adafruit/Adafruit_Python_PCA9685.git cd Adafruit_Python_PCA9685
sudo python setup.py install
```
