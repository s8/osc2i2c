import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

def read_pedal():
    if (ser.in_waiting >0):
        line = ser.readline()
        try:
            if line.strip():
                value = int(line.strip()) - 895
                value = min(1.0, float(value)/130)
                return value
        except ValueError:
            print ('serial value error')

while True:
    pedal_value = read_pedal()
    if pedal_value:
        print (pedal_value)

'''
while 1:
    if (ser.in_waiting > 0):
        line = ser.readline()
        
        try:
            if line.strip():
                value = int(line.strip())-895

                value = min(1.0, float(value)/130)
                print(value)
        except ValueError:
            print ('error')
'''     
     
