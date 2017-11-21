
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
    note = max(21, note)
    board = ((84-note) >> 4)
    channel = (note-21) % 16
    #print 'board: ', board, 'channel: ', channel
    return board, channel


# MIDI listener
with mido.open_input('Xkey:Xkey MIDI 1 20:0') as inport:
    for msg in inport:
        board, channel = note2motor(msg.note)
        
        print msg
        print 'board: ', board, 'channel: ', channel
        
        if msg.type == 'polytouch':
            pwm[board].set_pwm(channel, 0, msg.value*30)

        if msg.type == 'note_off':
            pwm[board].set_pwm(channel, 0, 0)

