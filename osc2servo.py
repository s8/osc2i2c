
# Adafruit PWM imports
from __future__ import division
import time
import Adafruit_PCA9685
import serial

# pyOSC imports
from OSC import OSCServer, OSCClient, OSCMessage
import sys
from time import sleep
import types
import os
import RPi.GPIO as GPIO

# Uncomment to enable debug output
#import logging
#logging.basicConfig*level=logging.DEBUG)

# Initialize the PCA9685 using the default address (0x40)

pwm = [
        Adafruit_PCA9685.PCA9685(0x40),
        Adafruit_PCA9685.PCA9685(0x41),
        Adafruit_PCA9685.PCA9685(0x42),
        Adafruit_PCA9685.PCA9685(0x43),
        Adafruit_PCA9685.PCA9685(0x44),
        Adafruit_PCA9685.PCA9685(0x45)
        ]

# DC motors
servo_min = 0
servo_max = 4095

# Helper function to make setting a servo pulse width simpler.

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= 60     # 60 Hz
    print ('{0}us per period'.format(pulse_length))
    pulse_length //= 4096   # 12 bits of resolution
    print ('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm[0].set_pwm(channel, 0, pulse)

# Set frequencey to 60hz, good for servos
for p in pwm:
    p.set_pwm_freq(60)


# Setting up Arduino on a serial port
ser = serial.Serial('/dev/ttyACM0',9600)
pedal_value = 0.0

def read_pedal():
    if (ser.int_waiting > 0):
        line = ser.readline()

    try:
        if line.strip():
            value = int(line.strip()) - 895
            value = min(1.0, float(value)/130)
            return (value)
    except ValueError:
        print ('serial value error')


# SETTING UP OSC Server and message handlers
# server = OSCServer (("192.168.1.2",57120))
# this has to be the address of Pi itself
# weirdly enough two sets of brackets are needed
# the port here has to match "outgoing" port on the controller app
# server = OSCServer(("192.168.1.6",8000))
server = OSCServer(("158.223.29.135",8000))
client = OSCClient()

def handle_timeout(self):
    print("I'm IDLE")

server.handle_timeout = types.MethodType(handle_timeout, server)

# fader handlers

def fader_callback(path, tags, args, source):
    pedal_update = read_pedal()
    if pedal_update:
        pedal_value = pedal_update
    motor = args[0]
    board = 5 - int(motor / 16)
    channel = int(motor % 16)
    value = int(pedal_value * args[1]*(servo_max-servo_min)+servo_min)

    pwm[board].set_pwm(channel,0,value)

    print "path: ", path, "motor: ", motor, "board: ", board,"channel: ", channel, "value: ", value

server.addMsgHandler( "/motor/", fader_callback)

while True:
    server.handle_request()

server.close()
