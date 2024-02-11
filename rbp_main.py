import network
import socket
import time
import secrets
from machine import Pin

# Create a Pin object for the onboard LED
onbled = machine.Pin("LED", machine.Pin.OUT)




ssid = secrets.SSID
password = secrets.PASSWORD
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

wlan.connect(ssid, password)
html = """<!DOCTYPE html>
<html>
    <head> <title>Rambo PI</title> </head>
        <body> <h1>LED Status Indicator</h1>
        <p>%s</p>

        </body>
</html>
"""
# Wait for connect or fail
max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

# Handle connection error
if wlan.status() != 3:
    raise RuntimeError('network connection failed')
else:
    print('connected')
    status = wlan.ifconfig()
    print( 'ip = ' + status[0] )

# Open socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)
# Listen for connections
while True:
    onbled.on()
    try:
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        print(request)
        request = str(request)
        led_on = request.find('/light/on')
        led_on2 = request.find('/light/on2')
        led_off = request.find('/light/off')
        print( 'led on = ' + str(led_on))
        print( 'led off = ' + str(led_off))

        if led_on == 6:
            try:
                with open('LED_ring.py', 'r') as f:
                    exec(f.read())
            except Exception as e:
                print ('Failed to execute script')
                print ('error: ', e)

        if led_off == 6:
            try:
                with open('turn_off_OLED.py', 'r') as f:
                    exec(f.read())
            except Exception as e:
                print ('Failed to execute script')
                print ('error: ', e)
                
                
        if led_on2 == 6:
            try:
                with open('LED_ring_breath.py', 'r') as f:
                    exec(f.read())
            except Exception as e:
                print ('Failed to execute script')
                print ('error: ', e)

        #response = html % stateis
        #cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        #cl.send(response)
        #cl.close()

    except OSError as e:
        cl.close()
        print('connection closed')