
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
pwm = [
        Adafruit_PCA9685.PCA9685(0x40),
        Adafruit_PCA9685.PCA9685(0x41),
        Adafruit_PCA9685.PCA9685(0x42),
        Adafruit_PCA9685.PCA9685(0x43)
        #Adafruit_PCA9685.PCA9685(0x44)
        #Adafruit_PCA9685.PCA9685(0x45)
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

# SETTING UP OSC Server and message handlers
# server = OSCServer (("192.168.1.2",57120))
# this has to be the address of Pi itself
# weirdly enough two sets of brackets are needed
# the port here has to match "outgoing" port on the controller app
server = OSCServer(("192.168.1.6",8000))
client = OSCClient()

def handle_timeout(self):
    print("I'm IDLE")

server.handle_timeout = types.MethodType(handle_timeout, server)

# fader handlers

def fader_callback(path, tags, args, source):

    # store the name of the TouchOSC interface element
    multifader = path.split("/")[2]
    
    fader_osc = int(path.split("/")[3]) - 1
    
    pwm_value = int(args[0]*(servo_max-servo_min)+servo_min)
    
    board_i2c = [fader_osc >> 4, fader_osc % 16, pwm_value];
    
    #if multifader == "multifader2":
    #    board_i2c[0] += 2

    pwm[board_i2c[0]].set_pwm(board_i2c[1],0,board_i2c[2])
    
    print "board: ", board_i2c[0], ", fader: ", board_i2c[1], ", value: ", board_i2c[2]

# origignal layout with 2 x32 multifaders
#for i in range(1,33):
#    server.addMsgHandler( "/1/multifader1/"+str(i), fader_callback)
#    server.addMsgHandler( "/1/multifader2/"+str(i), fader_callback)

for i in range(0,63):
    print 'registering callback for fader: ', i
    server.addMsgHandler( "/multifader/multifader/"+str(i), fader_callback)
    #server.addMsgHandler( "/1/multifader2/"+str(i), fader_callback)

while True:
    server.handle_request()

server.close()
