
#import pyo

#print pyo.pm_get_input_devices()[0][1]


import mido

with mido.open_input('Xkey:Xkey MIDI 1 20:0') as inport:
    for msg in inport:
        print msg
        if msg.type == 'polytouch':
            print 'note: ', msg.note, ' value: ', msg.value



