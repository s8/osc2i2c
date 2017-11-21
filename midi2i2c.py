
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

# midi imports
import mido

# Uncomment to enable debug output
#import logging
#logging.basicConfig*level=logging.DEBUG)

# Initialize the PCA9685 using the default address (0x40)
pwm = [
        Adafruit_PCA9685.PCA9685(0x41),
        Adafruit_PCA9685.PCA9685(0x42),
        Adafruit_PCA9685.PCA9685(0x43),
        Adafruit_PCA9685.PCA9685(0x44)
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
    for p in pwm: p.set_pwm(channel, 0, pulse)

# Set frequencey to 60hz, good for servos
for p in pwm: p.set_pwm_freq(60)

#
# MIDI
#

# note to board / channel mapper
def note2motor(note):
    #channel = max(0, note - 33)
    board = (96-note) >> 4
    channel = (96-note) % 16
    #print 'board: ', board, 'channel: ', channel
    return board, channel


# polytouch PWM setter
def polytouch2vibro(note, value):
    #board = int((63-note)/16)

    board, channel = note2motor(note)
    print 'POLYTOUCH board: ', board,'channel: ', channel, 'value: ', value*30, ' MIDI note: ', note
    
    pwm[board].set_pwm(channel, 0, value*30)

# note OFF
def motor_off(note):
    board, channel = note2motor(note)
    #board = int((63-note)/16)
    print 'NOTE OFF board: ', board, 'channel: ', channel, ' MIDI note: ', note
    pwm[board].set_pwm(note%16, 0, 0)

# MIDI listener
with mido.open_input('Xkey:Xkey MIDI 1 20:0') as inport:
    for msg in inport:
        print msg
        if msg.type == 'polytouch':
            #pwm[0].set_pwm(1,0,msg.value*30)
            polytouch2vibro(msg.note,msg.value)
            note2motor(msg.note)

        if msg.type == 'note_off':
            #print 'off'
            motor_off(msg.note)

     


#
# OSC
#


# SETTING UP OSC Server and message handlers
#server = OSCServer (("192.168.0.101",57120))
#client = OSCClient()

#def handle_timeout(self):
#    print("I'm IDLE")

#server.handle_timeout = types.MethodType(handle_timeout, server)

# fader handlers

#def fader_callback(path, tags, args, source):
#    multifader = path.split("/")[2]
    
#    fader_osc = int(path.split("/")[3]) - 1
    
#    pwm_value = int(args[0]*(servo_max-servo_min)+servo_min)
    
#    fader_i2c = [fader_osc >> 4, fader_osc % 16, pwm_value];
    
#    if multifader == "multifader2":
#        fader_i2c[0] += 2

#   pwm[fader_i2c[0]].set_pwm(fader_i2c[1],0,fader_i2c[2])
    
#    print "board: ", fader_i2c[0], ", fader: ", fader_i2c[1], ", value: ", fader_i2c[2]




# OSC message handlers
#for i in range(1,33):
#    server.addMsgHandler( "/1/multifader1/"+str(i), fader_callback)
#    server.addMsgHandler( "/1/multifader2/"+str(i), fader_callback)


#while True:
#    server.handle_request()

#server.close()
