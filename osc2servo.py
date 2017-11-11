
# Adafruit PWM imports
from __future__ import division
import time
import Adafruit_PCA9685

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
pwm = Adafruit_PCA9685.PCA9685()

# Configure min and max servo pulse lengths
servo_min = 100     # Min pulse length out of 4096
servo_max = 3095    # Max pulse length out of 4096

# PowerHD HD-1440A servo motor
servo_min = 135
servo_max = 630

# Helper function to make setting a servo pulse width simpler.

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000  # 1,000,000 us per second
    pulse_length //= 60     # 60 Hz
    print ('{0}us per period'.format(pulse_length))
    pulse_length //= 4096   # 12 bits of resolution
    print ('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequencey to 60hz, good for servos
pwm.set_pwm_freq(60)



#
# SETTING UP OSC Server and message handlers
#
server = OSCServer (("192.168.0.50",57120))
client = OSCClient()

def handle_timeout(self):
    print("I'm IDLE")

server.handle_timeout = types.MethodType(handle_timeout, server)

# fader handler
def fader_01(path, tags, args, source):
    #value = int(args[1])
    pwm_value = int(args[0]*(servo_max-servo_min) + servo_min)
    pwm.set_pwm(0,0,pwm_value)
    print "Fader Value:", pwm_value

# toggle handler
def toggle_01(path, tags, args, source):
    state=int(args[0])
    if state == 1:
        pwm.set_pwm(0,0,servo_max)
    else:
        pwm.set_pwm(0,0,servo_min)
    print "TOGGLE_01:", state


server.addMsgHandler("/1/toggle1", toggle_01)
server.addMsgHandler("/1/fader1", fader_01)
while True:
    server.handle_request()

server.close()
