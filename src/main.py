from machine import Pin, ADC, reset
import network
import ubinascii
import urequests as requests

import socket
from time import sleep

ldr = ADC(Pin(28))
led = Pin("LED", Pin.OUT)
LED_state = False

# WiFi data
ssid = 'ESSID'
password = 'PASSWORD'

# Mailgun data
KEY = 'MAILGUN-KEY'
SANDBOX = 'MAILGUN-SANDBOX'
sender = 'Notify Lock Alert <locker-alert@googlegroups.com>'
recipient = ["EMAIL LIST"]

# Send an email
def sendEmail():
    print('Sending alert email...')
    #data = {
    #    'from': sender,
    #    'to': recipient,
    #    'subject': 'Notificación de taquilla aberta',
    #    'text': 'A túa taquilla foi aberta.'
    #}
    data='from=Notify%20Lock%20Alert%20%3Clocker-alert%40googlegroups.com%3E&to=email%40udc.es'
    base_64 = ubinascii.b2a_base64('api:' + KEY).decode("utf-8").replace("\n", "")
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic %s' % base_64}
    request_url = f'https://api.mailgun.net/v3/{SANDBOX}/messages'
    request = requests.post(request_url, data=data, headers=headers)
    print(request.text)
    print(request.status_code)
    #if request.status_code == 200:
    #    print('Email notify was succesfully sent.')
    #    pritn(request.json())

# Connect to WiFi network
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

try:
    ip = connect()
except KeyboardInterrupt:
    machine.reset()
    
email_sent = False
while True:    
    print(ldr.read_u16())
    ldr_value = ldr.read_u16()
    if ldr_value < 40000:
        # Send Email
        if not email_sent:
            led.on()
            sendEmail()
        email_sent = True
    else:
        led.off()
        email_sent = False

    sleep(1)
