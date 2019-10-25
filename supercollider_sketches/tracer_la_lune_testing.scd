n = NetAddr("158.223.29.135",8000); // RPi on the local network

n.sendMsg("/1/1/2",0.5)

n.sendMsg("/motor/80",0.5)
n.sendMsg("/motor/80",0.0)

